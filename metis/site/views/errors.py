from django.shortcuts import render
from django.views.decorators.csrf import requires_csrf_token


# from sentry_sdk import capture_event


@requires_csrf_token
def server_error(request):
    return render(request, "500.html", {"sentry_event_id": ""}, status=500)
