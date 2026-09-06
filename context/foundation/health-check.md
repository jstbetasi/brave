---
project: no-bias-essay-grader
checked_at: 2026-09-06T15:37:52Z
health_status: needs-attention
context_type: brownfield
language_family: python
stack_assessment_available: false
checks_run:
  - lockfile
  - dependency_audit
  - outdated_deps
  - test_runner
  - ci_cd
  - configuration
audit_findings:
  critical: 0
  high: 0
  moderate: 0
  low: 0
test_runner_detected: true
ci_provider: null
recommended_fixes: 5
---

## Dependency Health

### Lockfile

Status: missing (true lock) — present (weak): `requirements.txt`
Package manager: uv (per `context/foundation/tech-stack.md`), but no `uv.lock` in the repo

`requirements.txt` pins most packages (`Django==6.1.1`, `asgiref==3.12.1`, `sqlparse==0.6.0`, `tzdata==2026.3`) but leaves two unpinned (`pip-audit`, `uv`), so builds are not fully reproducible. Fix: run `uv lock` to generate `uv.lock`, or at minimum pin the two unpinned entries in `requirements.txt`.

### Security Audit

Tool: `pip-audit --format json`
Summary: 0 CRITICAL, 0 HIGH, 0 MODERATE, 0 LOW
Direct vs transitive: not distinguished by this tool

No known vulnerabilities across all 34 resolved packages (direct + transitive).

### Outdated Dependencies

Packages with major version gaps: 0

One patch-level gap noted (not a fix item): `uv` 0.12.9 → 0.12.10.

## Test Suite

Test runner: Django's built-in test runner (`python manage.py test`, unittest-based)
Tests found: 16 tests
Test execution: passing

Configuration: no dedicated pytest/tox config — uses Django's built-in test discovery across `accounts/tests.py` and `grading/tests.py`.
Framework: Django 6.1.1 test framework (`django.test.TestCase`)

## CI/CD

Provider: not detected
Configuration: not found

ℹ No CI/CD configuration detected. You'll set this up in the infrastructure and deployment lesson. For now, a local test runner is sufficient for agent collaboration — and this project's is working (16/16 passing).

| Stage      | Status | Notes                                      |
|------------|--------|--------------------------------------------|
| Lint       | ✗      | not configured                              |
| Test       | ✗      | not wired to CI (runs locally via `manage.py test`) |
| Build      | ✗      | not configured                              |
| Type check | ✗      | not configured                              |
| Security   | ✗      | not configured (pip-audit available locally, not wired to CI) |

## Configuration

### High severity

- **`.gitignore` present but incomplete — `db.sqlite3` and compiled `__pycache__/*.pyc` files are tracked in git.** The dev database (containing real password hashes for the `admin`/`admin1` superuser accounts) and bytecode caches are committed to version control. This is the kind of gap that compounds fast in a project whose own PRD centers on data privacy (RODO). Fix: add `db.sqlite3`, `__pycache__/`, `*.pyc`, and `.env` to `.gitignore`, then `git rm --cached db.sqlite3 no_bias_essay_grader/__pycache__/*.pyc` to stop tracking them (this does not delete the local files, only removes them from future commits — full removal from git *history* is a separate, more invasive operation the user should decide on deliberately).

### Medium severity

- **No type-checking configured** — Python project with no `mypy` / `django-stubs` setup. `context/foundation/tech-stack.md` already flags this as a known gap ("`typed: false` flag on the Django card... addressable with `django-stubs` + `mypy`"). Fix: `pip install django-stubs mypy` and add a minimal `mypy.ini`.
- **No linter/formatter configured** — no `ruff`, `black`, or `flake8` config found. Agent-generated code has no automated style check to converge against. Fix: `pip install ruff` and add a `ruff.toml` (or `[tool.ruff]` in a new `pyproject.toml`).
- **Secrets and environment config are hardcoded, not externalized** — `no_bias_essay_grader/settings.py` has a hardcoded `SECRET_KEY`, `DEBUG = True`, and empty `ALLOWED_HOSTS`, with no `.env` / `.env.example` pattern in place. `AGENTS.md` already notes the `SECRET_KEY` must be replaced before any non-local deployment, but there's currently no mechanism (e.g. `django-environ` or `python-decouple`) to load it from environment variables. Fix: introduce `django-environ`, read `SECRET_KEY`/`DEBUG`/`ALLOWED_HOSTS` from the environment, and commit a `.env.example` documenting the expected variables (paired with the `.gitignore` fix above so a real `.env` is never committed).

### Low severity

- **`.editorconfig`** — not present. Minor: keeps formatting consistent across editors for a solo developer, lower priority than the items above.

All other checked configuration is present and in good shape: `.gitignore` exists (just incomplete, see above), and both `AGENTS.md` and `CLAUDE.md` are present with substantive, project-specific content — no gap there.

## Stack Assessment Cross-Reference

No stack-assessment.md found. Run `/10x-stack-assess` for quality-gate analysis.

(Note: `context/foundation/tech-stack.md` — from `/10x-tech-stack-selector`, not `/10x-stack-assess` — already documents the `typed: false` gap referenced above, and this health check corroborates it: no type-checking is present anywhere in the project, in or out of CI.)

## Recommended Fixes

### Fix before agent work (Category A)

### 1. Stop tracking `db.sqlite3` and `__pycache__` in git

**Impact**: The dev database (with real password hashes) and bytecode caches are in version control history. Every future commit risks leaking more real account/session data into a shared repo, and an agent working on this repo could unknowingly commit further real data changes.
**Severity**: high
**Effort**: quick (< 5 min)
**Fix**:

```bash
# add to .gitignore
echo "db.sqlite3" >> .gitignore
echo "__pycache__/" >> .gitignore
echo "*.pyc" >> .gitignore
echo ".env" >> .gitignore

git rm --cached db.sqlite3
git rm --cached no_bias_essay_grader/__pycache__/*.pyc
git commit -m "Stop tracking db.sqlite3 and __pycache__"
```

### 2. Generate a real lockfile

**Impact**: Two packages (`pip-audit`, `uv`) are unpinned in `requirements.txt`. An agent re-installing dependencies later could get a different version than what's running now, silently changing behavior.
**Severity**: medium
**Effort**: quick (< 5 min)
**Fix**:

```bash
uv lock
```

Commit the resulting `uv.lock`.

### 3. Externalize secrets and environment config

**Impact**: `SECRET_KEY` is hardcoded and committed; `DEBUG=True` and empty `ALLOWED_HOSTS` are the only settings available — there's no path to a safe production config, and no documented set of required environment variables for anyone (or any agent) picking up deployment work.
**Severity**: medium
**Effort**: moderate (15–30 min)
**Fix**:

```bash
uv pip install django-environ
```

Then read `SECRET_KEY`, `DEBUG`, and `ALLOWED_HOSTS` via `environ.Env()` in `settings.py`, and commit a `.env.example` listing the expected keys (paired with fix #1's `.gitignore` update).

### 4. Add type-checking

**Impact**: Agent-generated Django code (models, views, forms) has no static check catching type errors before they reach `manage.py test`. This is the gap `tech-stack.md` already flagged.
**Severity**: medium
**Effort**: moderate (15–30 min)
**Fix**:

```bash
uv pip install django-stubs mypy
```

Add a minimal `mypy.ini` with `plugins = mypy_django_plugin.main` and a `[mypy.plugins.django-stubs]` section pointing at `no_bias_essay_grader.settings`.

### 5. Add a linter/formatter

**Impact**: No automated style convergence for agent-written code — style drift accumulates silently across sessions.
**Severity**: medium
**Effort**: quick (< 5 min)
**Fix**:

```bash
uv pip install ruff
```

Add a `ruff.toml` (or `[tool.ruff]` block in a new `pyproject.toml`) and run `ruff check .` / `ruff format .`.

### Addressed in upcoming lessons (Category B)

### No CI/CD pipeline

**Lesson**: [Sprint Zero z Agentem: infrastruktura, walking skeleton i pierwszy deploy (M1L5)](https://platforma.przeprogramowani.pl/external/10xdevs-3/m1-l5)
**What you'll do there**: Set up GitHub Actions with the auto-deploy-on-merge flow already recorded as the intended CI provider in `context/foundation/tech-stack.md`, wiring in lint/test/build/security stages.

### No deployment configuration (Fly.io)

**Lesson**: [Sprint Zero z Agentem: infrastruktura, walking skeleton i pierwszy deploy (M1L5)](https://platforma.przeprogramowani.pl/external/10xdevs-3/m1-l5)
**What you'll do there**: Add `fly.toml` and the Fly.io deployment scaffolding for the target already chosen in `tech-stack.md`.

## Summary

Health status: needs-attention

The project's core signals are strong: zero known dependency vulnerabilities, a working test suite (16/16 passing) covering both the auth flow and the essay-grading rubric, and both `AGENTS.md`/`CLAUDE.md` already in good shape. The gaps are all addressable in well under an hour combined — the standout is `db.sqlite3` (containing real password hashes) being tracked in git, which is worth fixing before any further commits. The rest (lockfile, type-checking, linting, externalized secrets) are standard hardening steps that make agent-assisted changes easier to trust and reproduce.

Next step: address the Category A fixes above (starting with the `.gitignore`/`db.sqlite3` fix), then proceed to agent onboarding — you've effectively already done much of it (`AGENTS.md`/`CLAUDE.md` exist), so that step should mostly be a review rather than a from-scratch build.
