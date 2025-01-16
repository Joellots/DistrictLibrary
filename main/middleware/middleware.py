# middleware.py
from django.contrib.auth import logout
from django.utils import timezone
from datetime import datetime
from django.contrib import messages
from django.shortcuts import redirect


class SessionTimeoutMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            # Set the last activity time in the session
            last_activity = request.session.get('last_activity', None)
            if last_activity:
                last_activity_datetime = datetime.fromisoformat(last_activity)
                formatted_last_activity = datetime.strftime(last_activity_datetime, "%Y-%m-%d %H:%M:%S.%f%z")

                if datetime.strptime(formatted_last_activity, "%Y-%m-%d %H:%M:%S.%f%z") + timezone.timedelta(minutes=5) < datetime.strptime(str(timezone.now()), "%Y-%m-%d %H:%M:%S.%f%z"):
                    # If the user has been inactive for more than 15 minutes, log them out
                    logout(request)
                    messages.success(request, "Session Timed Out")
                    return redirect('login')
            else:
                request.session['last_activity'] = str(timezone.now())

        response = self.get_response(request)
        return response