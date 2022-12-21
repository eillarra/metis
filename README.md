# SPARTA

[![github-tests-badge]][github-tests]
[![codecov-badge]][codecov]
[![license-badge]](LICENSE)


The SPARTA api/website uses [Django][django] and the [Django REST Framework][drf].

### Application dependencies

The application uses [Pipenv][pipenv] to manage Python packages. While in development, you will need to install
all dependencies (includes packages like `debug_toolbar`):

```bash
pipenv install --dev
pipenv shell
```

Update dependencies (and manually update `requirements.txt`):

```bash
pipenv update --dev && pipenv lock && pipenv requirements
```

### Run the app in development mode

```bash
python manage.py runserver
```

### Run Huey worker

```bash
python manage.py run_huey
```

### Run the tests

```bash
pytest --cov=sparta --cov-report=term
```

### Style guide

Tab size is 4 spaces. Max line length is 120. You should run `flake8` and `black` before committing any change.

```bash
black sparta
```


[codecov]: https://app.codecov.io/gh/eillarra/sparta
[codecov-badge]: https://codecov.io/gh/eillarra/sparta/branch/master/graph/badge.svg?token=UAQVA8J7YS
[github-tests]: https://github.com/eillarra/sparta/actions?query=workflow%3Atests
[github-tests-badge]: https://github.com/eillarra/sparta/workflows/tests/badge.svg
[license-badge]: https://img.shields.io/badge/license-MIT-blue.svg


[django]: https://www.djangoproject.com/
[drf]: https://www.django-rest-framework.org/
[pipenv]: https://docs.pipenv.org/#install-pipenv-today
