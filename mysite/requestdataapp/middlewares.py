import time

from django.http import HttpRequest, HttpResponse
from django.core.cache import cache



def get_useragent_on_request_middleware(get_response):
    def middleware(request: HttpRequest):
        request.user_agent = request.META.get('HTTP_USER_AGENT', 'Unknown')
        response = get_response(request)
        return response
    return middleware



class CountRequestMiddleware:
    def __init__(self, get_response):
        self._get_response = get_response
        self._requests_count = 0
        self._response_count = 0
        self._exceptions_count = 0

    def __call__(self, request: HttpRequest):
        self._requests_count += 1
        response = self._get_response(request)
        self._response_count += 1
        return response


    def process_exception(self, request: HttpRequest, exception: Exception):
        self._exceptions_count += 1
        print(f'Exception couunt {self._exceptions_count}')


class ThrottingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.cache_timeout = 120


    def __call__(self, request: HttpRequest) -> HttpResponse:
        ip = request.META.get('REMOTE_ADDR')
        if not ip:
            return self.get_response(request)

        count = self.requests_by_minute(ip)

        if count >= 100:
            return HttpResponse(f'<h1>Request limit per minute exceeded for ip: {ip}</h1>')

        response = self.get_response(request)
        return response


    def requests_by_minute(self, ip: str) -> int:
        cur_time = int(time.time())
        cache_key = f'requests:{ip}'
        history = cache.get(cache_key, [])
        minute_ago = cur_time - 60
        history = [t for t in history if t > minute_ago]
        history.append(cur_time)
        cache.set(cache_key, history,self.cache_timeout)
        return len(history)




