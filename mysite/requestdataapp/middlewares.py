import time
from django.core.cache import cache
from django.http import JsonResponse, HttpRequest


class RateLimitMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.RATE_LIMIT = 5
        self.TIME_WINDOW = 10

    def __call__(self, request: HttpRequest):
        ip = request.META.get('REMOTE_ADDR')

        cache_key = f"rate_limit_{ip}"

        request_history = cache.get(cache_key, [])
        current_time = time.time()

        request_history = [t for t in request_history if current_time - t < self.TIME_WINDOW]

        if len(request_history) >= self.RATE_LIMIT:
            return JsonResponse(
                {"error": "Too many requests. Please try again later."},
                status=429
            )

        request_history.append(current_time)

        cache.set(cache_key, request_history, timeout=self.TIME_WINDOW)

        return self.get_response(request)
