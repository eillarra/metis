import os


def app(request):
    return {
        "CONTACT_EMAIL": "eneko.illarramendi@ugent.be",
    }


def sentry(request):
    return {
        "GIT_REV": os.environ.get("GIT_REV", None),
    }
