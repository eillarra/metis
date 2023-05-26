import os


def app(request):
    return {
        "DJANGO_ENV": os.environ.get("DJANGO_ENV", "development"),
        "CONTACT_EMAIL": "metis@ugent.be",
        "HELPDESK_EMAIL": "helpdesk.metis@ugent.be",
    }


def sentry(request):
    return {
        "GIT_REV": os.environ.get("GIT_REV", None),
    }
