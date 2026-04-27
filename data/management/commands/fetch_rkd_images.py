"""
Management command: fetch_rkd_images

Walks every Artist and Artwork record that has an rkd_link, calls the
research.rkd.nl detail API to discover the first IIIF image, and stores
a ready-to-use thumbnail URL in the rkd_image_url field.

Usage:
    python manage.py fetch_rkd_images            # skip already-populated records
    python manage.py fetch_rkd_images --force    # re-fetch all RKD-linked records
    python manage.py fetch_rkd_images --artists-only
    python manage.py fetch_rkd_images --artworks-only

Thumbnail size is 300x300 max (IIIF !300,300). Change THUMB_SIZE below to
adjust (e.g. '400,400', '500,500').
"""

import re
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


def extract_rkd_id(url):
    """Extract the numeric RKD ID from a rkd.nl URL."""
    m = re.search(r'/(\d+)/?$', url.strip())
    return m.group(1) if m else None


def fetch_first_iiif_thumbnail(data_url):
    """
    Call the RKD research API and return a thumbnail URL for the first image,
    or None if no images are available.
    """
    api_url = RKD_API.format(rkd_data_url=data_url)
    req = urllib.request.Request(api_url, headers={'User-Agent': 'DttG-db/1.0'})
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            data = json.loads(r.read())
    except (urllib.error.URLError, json.JSONDecodeError) as e:
        return None, str(e)

    images = data.get('images', [])
    if not images:
        return None, 'no images in API response'

    iiif_base = images[0].get('src', '')
    if not iiif_base:
        return None, 'empty src in first image'

    thumbnail_url = f'{iiif_base}/full/{THUMB_SIZE}/0/default.jpg'
    return thumbnail_url, None


class Command(BaseCommand):
    help = 'Populate rkd_image_url on Artists and Artworks from the RKD IIIF API.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--force',
            action='store_true',
            help='Re-fetch even for records that already have an rkd_image_url.',
        )
        parser.add_argument('--artists-only', action='store_true')
        parser.add_argument('--artworks-only', action='store_true')

    def handle(self, *args, **options):
        force = options['force']
        do_artists = not options['artworks_only']
        do_artworks = not options['artists_only']

        if do_artists:
            self._process(
                queryset=Artist.objects.filter(rkd_link__gt=''),
                data_url_template=ARTIST_DATA_URL,
                label='Artist',
                force=force,
            )

        if do_artworks:
            self._process(
                queryset=Artwork.objects.filter(rkd_link__gt=''),
                data_url_template=IMAGE_DATA_URL,
                label='Artwork',
                force=force,
            )

    def _process(self, queryset, data_url_template, label, force):
        if not force:
            queryset = queryset.filter(rkd_image_url='')

        total = queryset.count()
        self.stdout.write(f'\n{label}: {total} records to process.')

        ok = skipped = errors = 0

        for i, obj in enumerate(queryset, 1):
            rkd_id = extract_rkd_id(obj.rkd_link)
            if not rkd_id:
                self.stdout.write(
                    self.style.WARNING(f'  [{i}/{total}] {obj} — could not parse RKD ID from: {obj.rkd_link}')
                )
                skipped += 1
                continue

            data_url = data_url_template.format(id=rkd_id)
            thumbnail_url, err = fetch_first_iiif_thumbnail(data_url)

            if err:
                self.stdout.write(
                    self.style.WARNING(f'  [{i}/{total}] {obj} — {err}')
                )
                skipped += 1
            else:
                obj.rkd_image_url = thumbnail_url
                # Use update() to bypass the save() method that resizes local images
                type(obj).objects.filter(pk=obj.pk).update(rkd_image_url=thumbnail_url)
                self.stdout.write(
                    self.style.SUCCESS(f'  [{i}/{total}] {obj} — {thumbnail_url}')
                )
                ok += 1

            # Polite rate limit: ~6 requests/second
            time.sleep(0.17)

        self.stdout.write(
            f'\n{label} done: {ok} updated, {skipped} skipped/no-image, {errors} errors.\n'
        )
