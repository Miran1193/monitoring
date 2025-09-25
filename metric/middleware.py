from django.http import HttpResponse
import os

class SimpleAuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.api_key = os.environ.get('API_KEY', 'supersecretkey')

    def __call__(self, request):
        if request.path.startswith('/api') or request.path.startswith('/metrics'):
            if request.headers.get('X-API-KEY') != self.api_key:
                return HttpResponse('Unauthorized', status=401)
        return self.get_response(request)