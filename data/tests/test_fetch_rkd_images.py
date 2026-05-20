"""
Tests for the fetch_rkd_images management command.

Covers:
  - _is_no_access detection (src-based and accessStatus-based)
  - fetch_first_iiif_thumbnail selection logic (first valid, skip no-access, etc.)
  - Stale no-access URL cleared when API returns no valid image
"""

import json
from io import BytesIO
from unittest.mock import MagicMock, patch

from django.test import TestCase

from data.management.commands.fetch_rkd_images import (
    _NO_VALID_IMAGE,
    _is_no_access,
    fetch_first_iiif_thumbnail,
    THUMB_SIZE,
)

# ── helpers ──────────────────────────────────────────────────────────────────

NO_ACCESS_SRC = 'https://images.rkd.nl/static/no-access.svg'
VALID_SRC = 'https://media.rkd.nl/iiif/10205398'
VALID_THUMB = f'{VALID_SRC}/full/{THUMB_SIZE}/0/default.jpg'
SUBONLY_SRC = 'https://media.rkd.nl/iiif/10633354'  # SUBONLY — Naiveu; standard IIIF still public
RESTRICTED_SRC = 'https://media.rkd.nl/iiif/10656895'  # RKDONLY — normal URL but blocked


def _mock_urlopen(payload):
    """Return a context-manager mock that yields a readable JSON response."""
    body = json.dumps(payload).encode()
    cm = MagicMock()
    cm.__enter__ = MagicMock(return_value=BytesIO(body))
    cm.__exit__ = MagicMock(return_value=False)
    return cm


# ── _is_no_access ─────────────────────────────────────────────────────────────

class IsNoAccessTests(TestCase):
    # src-based fallback (no accessStatus)
    def test_detects_no_access_svg_in_src(self):
        self.assertTrue(_is_no_access(NO_ACCESS_SRC))

    def test_detects_uppercase_variant(self):
        self.assertTrue(_is_no_access('https://images.rkd.nl/static/No-Access.SVG'))

    def test_valid_src_not_flagged_without_status(self):
        self.assertFalse(_is_no_access(VALID_SRC))

    def test_empty_string_not_flagged(self):
        self.assertFalse(_is_no_access(''))

    # accessStatus-based (primary path)
    def test_nolim_status_not_flagged(self):
        self.assertFalse(_is_no_access(RESTRICTED_SRC, access_status='NOLIM'))

    def test_rkdonly_status_flagged(self):
        self.assertTrue(_is_no_access(RESTRICTED_SRC, access_status='RKDONLY'))

    def test_subonly_status_not_flagged(self):
        # SUBONLY images are publicly viewable via the standard IIIF thumbnail endpoint
        self.assertFalse(_is_no_access(VALID_SRC, access_status='SUBONLY'))

    def test_unknown_status_not_flagged(self):
        # Unknown future statuses are optimistically allowed to avoid false negatives
        self.assertFalse(_is_no_access(VALID_SRC, access_status='MEMBER'))

    def test_none_status_falls_back_to_src(self):
        # None means key absent → fall back to src-based check
        self.assertFalse(_is_no_access(VALID_SRC, access_status=None))
        self.assertTrue(_is_no_access(NO_ACCESS_SRC, access_status=None))


# ── fetch_first_iiif_thumbnail ────────────────────────────────────────────────

class FetchFirstIiifThumbnailTests(TestCase):

    def _call(self, payload):
        with patch('urllib.request.urlopen', return_value=_mock_urlopen(payload)):
            return fetch_first_iiif_thumbnail('https://data.rkd.nl/artists/12345')

    def test_returns_valid_url_for_nolim_image(self):
        url, err = self._call({'images': [{'src': VALID_SRC, 'accessStatus': 'NOLIM'}]})
        self.assertIsNone(err)
        self.assertEqual(url, VALID_THUMB)

    def test_returns_valid_url_for_subonly_image(self):
        """Naiveu pattern: SUBONLY images are publicly accessible via IIIF."""
        url, err = self._call({'images': [{'src': SUBONLY_SRC, 'accessStatus': 'SUBONLY'}]})
        self.assertIsNone(err)
        self.assertEqual(url, f'{SUBONLY_SRC}/full/{THUMB_SIZE}/0/default.jpg')

    def test_skips_rkdonly_first_uses_nolim_second(self):
        """Wouter Crabeth II pattern: RKDONLY first, NOLIM second."""
        url, err = self._call({'images': [
            {'src': RESTRICTED_SRC, 'accessStatus': 'RKDONLY'},
            {'src': VALID_SRC, 'accessStatus': 'NOLIM'},
        ]})
        self.assertIsNone(err)
        self.assertEqual(url, VALID_THUMB)

    def test_all_rkdonly_returns_sentinel(self):
        url, err = self._call({'images': [
            {'src': RESTRICTED_SRC, 'accessStatus': 'RKDONLY'},
        ]})
        self.assertIsNone(url)
        self.assertEqual(err, _NO_VALID_IMAGE)

    def test_src_fallback_skips_no_access_svg(self):
        """Images without accessStatus fall back to src-based check."""
        url, err = self._call({'images': [
            {'src': NO_ACCESS_SRC},
            {'src': VALID_SRC},
        ]})
        self.assertIsNone(err)
        self.assertEqual(url, VALID_THUMB)

    def test_all_no_access_svg_returns_sentinel(self):
        url, err = self._call({'images': [{'src': NO_ACCESS_SRC}]})
        self.assertIsNone(url)
        self.assertEqual(err, _NO_VALID_IMAGE)

    def test_empty_images_list_returns_sentinel(self):
        url, err = self._call({'images': []})
        self.assertIsNone(url)
        self.assertEqual(err, _NO_VALID_IMAGE)

    def test_missing_images_key_returns_sentinel(self):
        url, err = self._call({})
        self.assertIsNone(url)
        self.assertEqual(err, _NO_VALID_IMAGE)

    def test_empty_src_in_only_image_returns_sentinel(self):
        url, err = self._call({'images': [{'src': '', 'accessStatus': 'NOLIM'}]})
        self.assertIsNone(url)
        self.assertEqual(err, _NO_VALID_IMAGE)

    def test_network_error_returns_error_string(self):
        with patch('urllib.request.urlopen', side_effect=OSError('connection refused')):
            url, err = fetch_first_iiif_thumbnail('https://data.rkd.nl/artists/99999')
        self.assertIsNone(url)
        self.assertIn('connection refused', err)
        self.assertNotEqual(err, _NO_VALID_IMAGE)
