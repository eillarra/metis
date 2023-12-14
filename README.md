# METIS

[![github-tests-py-badge]][github-tests-py]
[![codecov-badge]][codecov]
[![license-badge]](LICENSE)


## Backend

The Metis api/website uses [Django][django] and the [Django REST Framework][drf].

### Application dependencies

The application uses [Poetry][poetry] to manage application dependencies.

```bash
poetry lock
poetry install --sync --no-root
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
pytest --cov=metis --cov-report=term
```

### Style guide

Tab size is 4 spaces. Max line length is 120. You should run `ruff` before committing any change.

```bash
ruff format . && ruff check metis
```

## Frontend

Some parts of the website are developed as one page applications with [Vue][vue] (`vue` folder).
When working on these, it is necessary to start a node server in parallel, so Django can access the
modules via [Inertia][inertia].

```bash
yarn
yarn dev
```


[codecov]: https://app.codecov.io/gh/eillarra/metis
[codecov-badge]: https://codecov.io/gh/eillarra/metis/branch/main/graph/badge.svg?token=xZLoEWNzgu
[github-tests-py]: https://github.com/eillarra/metis/actions?query=workflow%3Atests-py
[github-tests-py-badge]: https://github.com/eillarra/metis/actions/workflows/tests_py.yml/badge.svg?branch=main
[license-badge]: https://img.shields.io/badge/license-MIT-blue.svg

[django]: https://www.djangoproject.com/
[drf]: https://www.django-rest-framework.org/
[inertia]: https://inertiajs.com/
[poetry]: https://python-poetry.org/
[vue]: https://vuejs.org/
