# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

Django project (`automation` = project config, `dataentry` = the only app) for automating data import/export between CSV files and database models. Styled with Tailwind CSS v4 + Flowbite. No tests exist yet (`dataentry/tests.py` is empty).

## Commands

```bash
source .venv/bin/activate
python manage.py runserver
python manage.py migrate

# Custom management commands (dataentry/management/commands/)
python manage.py importdata <csv_path> <ModelName>   # e.g. external_data/student_data.csv Student
python manage.py exportdata <ModelName>               # writes exported_<Model>_data_<timestamp>.csv to CWD
python manage.py insertdata                           # seeds Student rows
python manage.py test                                 # run tests (none yet); add a dotted path for a single test

# Tailwind (run alongside runserver; output static/css/style.css is generated)
npm run dev     # watch mode
npm run prod    # minified build
```

Settings read `SECRET_KEY`, `DEBUG`, `ALLOWED_HOSTS` from `.env` via `django-environ` (`SECRET_KEY` is required).

## Architecture

- `automation/urls.py` includes `dataentry.urls` at the site root; views: `home` and `import_data`.
- Model lookup is generic: `importdata`/`exportdata` take a model name string and search **all installed apps** with `apps.get_model`, so they work for any model (currently `Student`, `Customer` in `dataentry/models.py`). CSV headers must match model field names, since import does `model.objects.create(**row)`.
- `dataentry/utils.py:get_all_custom_models()` lists non-Django-builtin model names (filters a hardcoded exclusion list); used by the `import_data` view to populate the model dropdown. The POST branch of `import_data` is unimplemented (returns `None`).
- Templates: project-wide `templates/base.html` (the layout) plus app templates in `dataentry/templates/dataentry/`. Static files live in the root `static/` (`STATICFILES_DIRS`), including a vendored `static/js/flowbite.min.js`.
- Tailwind source is `static/css/input.css`; it scans `templates/` and `**/templates` for classes. After adding new utility classes to templates, rebuild `style.css`.

## Gotchas

- `importdata.py` doesn't `break` after finding the model (`exportdata.py` does), so with multiple apps having the same model name the last match wins.
- `db.sqlite3` is gitignored; exported CSVs land in the repo root.
