"""
Management command: fetch_rkd_images

Walks every Artist and Artwork record that has an rkd_link, calls the
research.rkd.nl detail API to discover the first valid IIIF image, and stores
a ready-to-use thumbnail URL in the rkd_image_url field.

Images marked as no-access by RKD (src contains 'no-access.svg') are skipped.
The command picks the first valid image in RKD API order, so a second image is
automatically used when the first is a no-access placeholder.

If no valid RKD image is found for a record that already holds a stale no-access
URL, the field is cleared so templates fall back to the DttG default local image.

Usage:
    python manage.py fetch_rkd_images            # skip already-populated (non-stale) records
    python manage.py fetch_rkd_images --force    # re-fetch all RKD-linked records
    python manage.py fetch_rkd_images --dry-run
    python manage.py fetch_rkd_images --max-updates 10
    python manage.py fetch_rkd_images --until-stable
    python manage.py fetch_rkd_images --artists-only
    python manage.py fetch_rkd_images --artworks-only

Thumbnail size is 300x300 max (IIIF !300,300). Change THUMB_SIZE below to
adjust (e.g. '400,400', '500,500').
"""

import re
import ssl
import time
import urllib.request
import urllib.error
import json

from django.core.management.base import BaseCommand
from data.models import Artist, Artwork

# IIIF thumbnail size — !WxH means 'fit within WxH, preserve aspect ratio'
THUMB_SIZE = '!300,300'

RKD_API = 'https://research.rkd.nl/api/detail?id={rkd_data_url}'
ARTIST_DATA_URL = 'https://data.rkd.nl/artists/{id}'
IMAGE_DATA_URL = 'https://data.rkd.nl/images/{id}'

# Build an SSL context that works reliably on macOS Python installs.
# certifi ships with the venv (pulled in transitively); if somehow absent,
# fall back to the default system context.
try:
    import certifi as _certifi
    _SSL_CTX = ssl.create_default_context(cafile=_certifi.where())
except ImportError:
    _SSL_CTX = ssl.create_default_context()

# Sentinel returned when no valid image is found but the API call itself succeeded
_NO_VALID_IMAGE = 'no-valid-image'


def extract_rkd_id(url):
    """Extract the numeric RKD ID from a rkd.nl URL."""
    m = re.search(r'/(\d+)/?$', url.strip())
    return m.group(1) if m else None


def _is_no_access(src, access_status=None):
    """
    Return True if the image should be skipped.

    RKD uses an 'accessStatus' field in the images array. Known values:
      NOLIM   – no restrictions; publicly accessible.
      SUBONLY – subscriber-quality, but the standard IIIF thumbnail is still public.
      RKDONLY – restricted; the IIIF endpoint serves a no-access.svg placeholder.

    Only RKDONLY is blocked. All other statuses (including unknown future ones)
    are treated as accessible to avoid false negatives.

    When accessStatus is absent we fall back to checking for 'no-access.svg'
    in the src URL (kept for backwards-compatibility with any cached responses).
    """
    if access_status is not None:
        return access_status == 'RKDONLY'
    return 'no-access.svg' in src.lower()


def fetch_first_iiif_thumbnail(data_url):
    """
    Call the RKD research API and return a thumbnail URL for the first *valid*
    image found in the response.  Images whose src contains 'no-access.svg' are
    skipped.  Returns (url, None) on success or (None, reason) on failure.

    The reason string is the module-level _NO_VALID_IMAGE sentinel when the API
    responded normally but every image was a no-access placeholder (or there were
    no images at all); callers can check for that sentinel to decide whether to
    clear a previously-saved stale URL.
    """
    api_url = RKD_API.format(rkd_data_url=data_url)
    req = urllib.request.Request(api_url, headers={'User-Agent': 'DttG-db/1.0'})
    try:
        with urllib.request.urlopen(req, timeout=10, context=_SSL_CTX) as r:
            data = json.loads(r.read())
    except Exception as e:
        return None, str(e)

    images = data.get('images', [])
    if not images:
        return None, _NO_VALID_IMAGE

    for img in images:
        iiif_base = img.get('src', '')
        access_status = img.get('accessStatus')
        if not iiif_base or _is_no_access(iiif_base, access_status):
            continue
        thumbnail_url = f'{iiif_base}/full/{THUMB_SIZE}/0/default.jpg'
        return thumbnail_url, None

    # Every image was a no-access placeholder
    return None, _NO_VALID_IMAGE


class Command(BaseCommand):
    help = 'Populate rkd_image_url on Artists and Artworks from the RKD IIIF API.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--force',
            action='store_true',
            help='Re-fetch even for records that already have an rkd_image_url.',
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Only report how many records would be processed; do not call the RKD API or save anything.',
        )
        parser.add_argument(
            '--max-updates',
            type=int,
            default=None,
            help='Stop after this many successful image updates for each selected model.',
        )
        parser.add_argument(
            '--until-stable',
            action='store_true',
            help='Repeat passes until no new URLs are fetched, then stop automatically.',
        )
        parser.add_argument('--artists-only', action='store_true')
        parser.add_argument('--artworks-only', action='store_true')

    def handle(self, *args, **options):
        force = options['force']
        dry_run = options['dry_run']
        max_updates = options['max_updates']
        until_stable = options['until_stable']
        do_artists = not options['artworks_only']
        do_artworks = not options['artists_only']

        if until_stable and dry_run:
            self.stdout.write(self.style.WARNING('--until-stable is ignored in --dry-run mode.'))

        if until_stable and force:
            self.stdout.write(self.style.WARNING('--until-stable with --force may run indefinitely; proceeding anyway.'))

        pass_no = 0
        while True:
            pass_no += 1
            self.stdout.write(self.style.NOTICE(f'\n=== fetch_rkd_images pass {pass_no} ==='))
            fetched_this_pass = 0

            if do_artists:
                fetched_this_pass += self._process(
                    queryset=Artist.objects.filter(rkd_link__gt=''),
                    data_url_template=ARTIST_DATA_URL,
                    label='Artist',
                    force=force,
                    dry_run=dry_run,
                    max_updates=max_updates,
                )

            if do_artworks:
                fetched_this_pass += self._process(
                    queryset=Artwork.objects.filter(rkd_link__gt=''),
                    data_url_template=IMAGE_DATA_URL,
                    label='Artwork',
                    force=force,
                    dry_run=dry_run,
                    max_updates=max_updates,
                )

            if not until_stable or dry_run:
                break

            if fetched_this_pass == 0:
                self.stdout.write(self.style.SUCCESS('\nNo new URLs fetched in this pass; stopping (stable state reached).'))
                break

            self.stdout.write(self.style.NOTICE(f'\nFetched {fetched_this_pass} new URL(s) in pass {pass_no}; starting another pass...'))

    def _process(self, queryset, data_url_template, label, force, dry_run, max_updates):
        if not force:
            # Always include records with a stale no-access URL so they are
            # corrected automatically, even if rkd_image_url is non-empty.
            queryset = queryset.filter(
                rkd_image_url=''
            ) | queryset.filter(
                rkd_image_url__icontains='no-access.svg'
            )

        total = queryset.count()
        self.stdout.write(f'\n{label}: {total} records to process.')

        if dry_run:
            stale = queryset.model.objects.filter(
                rkd_link__gt='', rkd_image_url__icontains='no-access.svg'
            ).count()
            self.stdout.write(
                f'{label} dry run: no API calls made, no records updated.'
                f' ({stale} stale no-access URL(s) would be reprocessed)\n'
            )
            return 0

        ok = cleared = skipped = errors = 0

        for i, obj in enumerate(queryset, 1):
            rkd_id = extract_rkd_id(obj.rkd_link)
            if not rkd_id:
                self.stdout.write(
                    self.style.WARNING(f'  [{i}/{total}] {obj} — could not parse RKD ID from: {obj.rkd_link}')
                )
                skipped += 1
                continue

            data_url = data_url_template.format(id=rkd_id)

            try:
                thumbnail_url, err = fetch_first_iiif_thumbnail(data_url)
            except Exception as exc:
                self.stdout.write(
                    self.style.WARNING(f'  [{i}/{total}] {obj} — unexpected error: {exc}')
                )
                errors += 1
                continue

            if thumbnail_url:
                # Use update() to bypass the save() method that resizes local images
                type(obj).objects.filter(pk=obj.pk).update(rkd_image_url=thumbnail_url)
                self.stdout.write(
                    self.style.SUCCESS(f'  [{i}/{total}] {obj} — updated: {thumbnail_url}')
                )
                ok += 1

                if max_updates and ok >= max_updates:
                    self.stdout.write(
                        self.style.SUCCESS(
                            f'  Reached max-updates={max_updates}; stopping {label.lower()} run early.'
                        )
                    )
                    break

            elif err == _NO_VALID_IMAGE:
                # API responded but no valid (non-no-access) image exists.
                # If the record has any existing rkd_image_url (stale), clear it
                # so templates fall back to the DttG default local image.
                if obj.rkd_image_url:
                    type(obj).objects.filter(pk=obj.pk).update(rkd_image_url='')
                    self.stdout.write(
                        self.style.WARNING(
                            f'  [{i}/{total}] {obj} — cleared stale URL (no valid RKD image available)'
                        )
                    )
                    cleared += 1
                else:
                    self.stdout.write(
                        self.style.WARNING(f'  [{i}/{total}] {obj} — no valid RKD image available; skipped')
                    )
                    skipped += 1

            else:
                # Network/API error — leave existing value untouched
                self.stdout.write(
                    self.style.WARNING(f'  [{i}/{total}] {obj} — API/network error: {err}')
                )
                skipped += 1

            # Polite rate limit: ~6 requests/second
            time.sleep(0.17)

        self.stdout.write(
            f'\n{label} done: {ok} updated, {cleared} stale no-access URLs cleared,'
            f' {skipped} skipped/no-image, {errors} errors.\n'
        )
        return ok
