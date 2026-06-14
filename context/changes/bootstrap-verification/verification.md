---
bootstrapped_at: 2026-05-25T00:00:00Z
starter_id: django
starter_name: Django
project_name: no-bias-essay-grader
language_family: python
package_manager: uv (not found in PATH — pip used as fallback for pre-step)
cwd_strategy: native-cwd
bootstrapper_confidence: verified
phase_3_status: ok
audit_command: pip-audit --format json
---

## Hand-off

```yaml
starter_id: django
package_manager: uv
project_name: no-bias-essay-grader
hints:
  language_family: python
  team_size: solo
  deployment_target: fly
  ci_provider: github-actions
  ci_default_flow: auto-deploy-on-merge
  bootstrapper_confidence: verified
  path_taken: standard
  quality_override: false
  self_check_answers: null
  has_auth: true
  has_payments: false
  has_realtime: false
  has_ai: false
  has_background_jobs: false
```

### Why this stack

Django is the recommended default for `(web-app, python)` and a clean fit for a 3-week, after-hours MVP with small-scale users. It ships auth, ORM, admin, and migrations out of the box — every structural need in the PRD is covered without third-party additions. Auth (FR-001–003: register, login, logout) maps directly to `django.contrib.auth`; no external auth library needed for MVP. The short timeline and after-hours constraint favor a batteries-included stack with verified bootstrapper confidence to eliminate setup overhead. Fly.io is the starter's default deployment target; GitHub Actions with auto-deploy-on-merge matches solo-developer discipline. The `typed: false` flag on the Django card is a known gap — addressable with `django-stubs` + `mypy` and a CLAUDE.md annotation if typed-agent coverage becomes a priority.

## Pre-scaffold verification

| Signal      | Value                                                    | Severity | Notes                                                         |
| ----------- | -------------------------------------------------------- | -------- | ------------------------------------------------------------- |
| npm package | not run                                                  | n/a      | Python starter — no npm package to check                      |
| GitHub repo | not run                                                  | n/a      | docs_url is https://docs.djangoproject.com (not a GitHub URL) |

No recency signal available for this starter. Django is a mature, actively maintained framework; check https://www.djangoproject.com/download/ for the current release.

## Scaffold log

**Resolved invocation**: `django-admin startproject no_bias_essay_grader .`
**Strategy**: native-cwd (scaffold directly into the current directory)
**Exit code**: 0
**Pre-flight files-to-touch**: manage.py, no_bias_essay_grader/__init__.py, no_bias_essay_grader/asgi.py, no_bias_essay_grader/settings.py, no_bias_essay_grader/urls.py, no_bias_essay_grader/wsgi.py
**Files written by CLI**: 6
**Pre-existing files preserved**: none (CLAUDE.md was in cwd but Django's startproject did not touch it)

### Toolchain note

`uv` (the package manager specified in the hand-off) was not found in PATH. The `pre` step (`pip install django`) was executed using the `.venv`'s `pip` as a fallback. Django 6.0.5 was installed successfully. Install `uv` (`pip install uv` or via the official installer at https://docs.astral.sh/uv/getting-started/installation/) to use the intended package manager for ongoing development.

### Name substitution note

Django's `cmd_template` (`django-admin startproject {name} .`) uses `{name}` as the Python module name, not the target directory — the `.` at the end of the template is already the directory argument. For `native-cwd`, `{name}` was resolved to `no_bias_essay_grader` (project_name `no-bias-essay-grader` sanitized to a valid Python identifier by replacing hyphens with underscores).

## Post-scaffold audit

**Tool**: pip-audit --format json
**Status**: failed to run
**Reason**: pip-audit not found in .venv/Scripts — tool not installed in the project virtualenv

Install pip-audit to run the audit: `pip install pip-audit` (or `uv pip install pip-audit` once uv is available). Then run `pip-audit --format json` from cwd.

## Hints recorded but not acted on

| Hint                    | Value              |
| ----------------------- | ------------------ |
| bootstrapper_confidence | verified           |
| quality_override        | false              |
| path_taken              | standard           |
| self_check_answers      | null               |
| team_size               | solo               |
| deployment_target       | fly                |
| ci_provider             | github-actions     |
| ci_default_flow         | auto-deploy-on-merge |
| has_auth                | true               |
| has_payments            | false              |
| has_realtime            | false              |
| has_ai                  | false              |
| has_background_jobs     | false              |

These hints were read from the hand-off and staged into this log. No automated action was taken on them in v1. A future M1L4 skill ("Memory Architecture") will act on these to generate CLAUDE.md and AGENTS.md tailored to the project's feature set.

## Next steps

Next: a future skill will set up agent context (CLAUDE.md, AGENTS.md). For now, your project is scaffolded and verified — happy hacking.

Useful manual steps in the meantime:
- `git init` (if you have not already) to start your own repo history.
- Install `uv` and run `uv pip install -r requirements.txt` (or configure a `pyproject.toml`) to align with the intended package manager.
- Install `pip-audit` and run the security audit: `pip install pip-audit && pip-audit --format json`.
- Run `python manage.py migrate` to apply the initial Django migrations.
- Run `python manage.py createsuperuser` to create the first admin user (has_auth = true).
- Review the scaffolded `no_bias_essay_grader/settings.py` — update SECRET_KEY, ALLOWED_HOSTS, and DATABASE for your environment.
