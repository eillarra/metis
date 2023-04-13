import os


def app(request):
    return {
        "CONTACT_EMAIL": "epione@ugent.be",
        "HELPDESK_EMAIL": "helpdesk.epione@ugent.be",
    }


def sentry(request):
    return {
        "GIT_REV": os.environ.get("GIT_REV", None),
    }
