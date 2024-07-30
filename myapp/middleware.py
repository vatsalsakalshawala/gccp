import json
from django.utils import timezone

class LoginTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        
        if request.user.is_authenticated:
            login_time = request.session.get('login_time')
            if not login_time:
                login_time = timezone.now().strftime('%Y-%m-%d %H:%M:%S')
                request.session['login_time'] = login_time
                response.set_cookie('login_time', login_time, max_age=3600)  # Cookie expires in 1 hour

        return response
