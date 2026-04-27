from django.conf import settings


class FrameAncestorsCSPMiddleware:
    """
    Adds a CSP frame-ancestors directive when FRAME_ANCESTORS is configured.

    This is used instead of X-Frame-Options because X-Frame-Options does not
    support an allowlist of multiple external domains in modern browsers.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        frame_ancestors = getattr(settings, 'FRAME_ANCESTORS', [])
        if not frame_ancestors:
            return response

        if 'Content-Security-Policy' not in response:
            response['Content-Security-Policy'] = f"frame-ancestors 'self' {' '.join(frame_ancestors)}"
        return response
