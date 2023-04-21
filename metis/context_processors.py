import os


def app(request):
    return {
        "CONTACT_EMAIL": "metis@ugent.be",
        "HELPDESK_EMAIL": "helpdesk.metis@ugent.be",
    }


def sentry(request):
    return {
        "GIT_REV": os.environ.get("GIT_REV", None),
    }
