# AGENTS.md

This file provides guidance to AI agents when working with code in this repository.

## Domain constraints (non-obvious)

- **No essay persistence** — essays submitted for grading must not be written to the database. RODO compliance is a hard requirement. Only the computed grade and metadata (teacher, timestamp, grade level) may be stored.
- **Rubric categories (Polish names are canonical):** `forma`, `argumentacja`, `język`, `struktura`. Each maps to a point range on a 1–6 scale. Do not anglicise these names in code or templates.
- **Flat auth model** — email + password only. No roles, no groups, no permissions hierarchy.
- **UI language is Polish** — all user-facing strings, form labels, and error messages must be in Polish. English is for code identifiers only.

## Commands

```bash
# Development server
python manage.py runserver

# Apply migrations
python manage.py migrate

# Create new migrations after model changes
python manage.py makemigrations

# Run tests
python manage.py test

# Open Django shell
python manage.py shell

# Install dependencies (uv preferred; fall back to pip if uv not in PATH)
uv pip install -r requirements.txt
# or
pip install -r requirements.txt
```

## Architecture

Single Django project package: `no_bias_essay_grader/` (settings, urls, wsgi, asgi). No custom apps have been created yet — all domain logic should live in new apps added under the project root.

**Database:** SQLite (`db.sqlite3`) during development; no migrations have been applied yet.

**Intended deployment target:** Fly.io with GitHub Actions CI (auto-deploy on merge to main).

## Project

**no_bias_essay_grader** — a Django web app for Polish school teachers to grade student essays without authorship bias. Evaluates essays across four rubric categories; outputs a numeric grade and allows CSV export. RODO-compliant: essays are never stored permanently.

## Key reference files

- @context/foundation/prd.md — full product requirements (Polish); authoritative for rubric, grade scale, and privacy rules
- @context/foundation/tech-stack.md — stack decisions and rationale (Django, uv, Fly.io, GitHub Actions)
- @no_bias_essay_grader/settings.py — Django configuration (SECRET_KEY is a placeholder; replace before any non-local deployment)
