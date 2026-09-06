---
bootstrapped_at: 2026-09-06T10:14:12Z
starter_id: django
starter_name: Django
project_name: no-bias-essay-grader
language_family: python
package_manager: uv
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

| Signal      | Value   | Severity | Notes                                                          |
| ----------- | ------- | -------- | --------------------------------------------------------------- |
| npm package | not run | n/a      | Python starter — no npm package to check                       |
| GitHub repo | not run | n/a      | docs_url is https://docs.djangoproject.com (not a GitHub URL)   |

No recency signal available for this starter. Django is a mature, actively maintained framework; check https://www.djangoproject.com/download/ for the current release.

## Scaffold log

**Resolved invocation**: `django-admin startproject no_bias_essay_grader .`
**Strategy**: native-cwd (scaffold directly into the current directory)
**Exit code**: 0
**Pre-flight files-to-touch**: manage.py, no_bias_essay_grader/__init__.py, no_bias_essay_grader/asgi.py, no_bias_essay_grader/settings.py, no_bias_essay_grader/urls.py, no_bias_essay_grader/wsgi.py
**Files written by CLI**: 6
**Pre-existing files preserved**: none

### Re-run note

This is a re-run of bootstrapper against a directory that had already been bootstrapped once (see git history / commit `ed15867`, "first commit"). An earlier retry in this same session hard-stopped because `manage.py` still existed (Django 6.0.5 now refuses to overlay a project onto an existing `manage.py` — a stricter check than the version used in the original run). Before this retry, the conflicting files (`manage.py`, `no_bias_essay_grader/`, `db.sqlite3`) were removed from the working tree (not by bootstrapper), clearing the conflict so `django-admin startproject` could complete normally. `requirements.txt`, `CLAUDE.md`, and `AGENTS.md` were left in place throughout and were not touched by the scaffold CLI.

### Toolchain note

Unlike the original run, `uv` and `pip-audit` are both present in `.venv/Scripts/` this time — no fallback was needed for either the install step or the audit step.

## Post-scaffold audit

**Tool**: pip-audit --format json
**Summary**: 0 CRITICAL, 0 HIGH, 14 MODERATE, 0 LOW
**Direct vs transitive**: not distinguished by this tool

All 14 findings default to MODERATE per the tiering rule (pip-audit carries no native severity field, and no advisory text explicitly names CRITICAL or HIGH).

#### MODERATE findings

**django 6.0.5** (9 advisories, fix in 5.2.15/6.0.6, 5.2.16/6.0.7, or 5.2.17/6.0.8 depending on advisory):
- PYSEC-2026-199 / CVE-2026-6873 — `get_signed_cookie` non-injective salt derivation allows cookie reuse across different `(name, salt)` contexts. Fix: 5.2.15, 6.0.6.
- PYSEC-2026-197 / CVE-2026-35193 — `UpdateCacheMiddleware` omits `Authorization` from `Vary`, risking private cache leakage. Fix: 5.2.15, 6.0.6.
- PYSEC-2026-200 / CVE-2026-7666 — SMTP `EmailBackend` can reuse a partially-initialized connection after a failed STARTTLS handshake with `fail_silently=True`, exposing email content in cleartext. Fix: 5.2.15, 6.0.6.
- PYSEC-2026-198 / CVE-2026-48587 — `has_vary_header()` doesn't strip whitespace from `Vary` values before comparison, allowing cache-key mismatches. Fix: 5.2.15, 6.0.6.
- PYSEC-2026-201 / CVE-2026-8404 — `UpdateCacheMiddleware` matches `Cache-Control` directives case-sensitively, allowing incorrect caching of uppercase/mixed-case directives. Fix: 5.2.15, 6.0.6.
- PYSEC-2026-2090 / CVE-2026-48588 — `UpdateCacheMiddleware`/`cache_page()` cache cookie-varying responses even when unrelated cookies are present, leaking private data via shared cache. Fix: 5.2.16, 6.0.7.
- PYSEC-2026-2092 / CVE-2026-53878 — `DomainNameValidator` allows newlines, enabling HTTP header injection if used directly in a response header. Fix: 5.2.16, 6.0.7.
- PYSEC-2026-2091 / CVE-2026-53877 — GeoDjango's `GDALRaster` over-reads its buffer when constructed from bytes, risking memory disclosure or segfault. Fix: 5.2.16, 6.0.7.
- PYSEC-2026-3717 / CVE-2026-15830 — GeoDjango's `GEOSGeometry` unbounded recursion on deeply-nested WKT/WKB/GEOMETRYCOLLECTION input can segfault (DoS). Fix: 5.2.17, 6.0.8.

**sqlparse 0.5.5** (5 advisories, all fixed in 0.6.0; transitive dependency of Django's ORM):
- PYSEC-2026-3698 / CVE-2026-59893 — ReDoS in the dollar-quoted-literal and multiline-comment lexer regexes (ostensibly O(n²) on unmatched delimiters).
- PYSEC-2026-3697 / CVE-2026-71491 — O(n²) comment-grouping causes CPU DoS on comment-heavy SQL text.
- PYSEC-2026-3699 / CVE-2026-54284 — Quadratic `TokenList.__str__` flattening lets small deeply-nested SQL (parens/CASE) burn seconds of CPU before the token/depth caps trigger.
- PYSEC-2026-3696 / CVE-2026-59894 — Python/PHP snippet output modes (`output_format='python'|'php'`) escape quotes without escaping existing backslashes first, enabling source-code injection if the generated snippet is later executed.
- CVE-2026-84305 — `ReindentFilter` offset recalculation is quadratic on tuple-list reindentation, allowing CPU DoS via `reindent=True` on crafted input.

None of these findings are reachable through this project's current code (a freshly scaffolded Django project makes no use of `reindent`/output-snippet modes and does not parse untrusted SQL text directly), but they should be tracked before any feature exposes SQL formatting, cache middleware, or GIS functionality to user input.

## Hints recorded but not acted on

| Hint                    | Value                 |
| ----------------------- | --------------------- |
| bootstrapper_confidence | verified              |
| quality_override        | false                 |
| path_taken              | standard              |
| self_check_answers      | null                  |
| team_size               | solo                  |
| deployment_target       | fly                   |
| ci_provider             | github-actions        |
| ci_default_flow         | auto-deploy-on-merge  |
| has_auth                | true                  |
| has_payments            | false                 |
| has_realtime            | false                 |
| has_ai                  | false                 |
| has_background_jobs     | false                 |

These hints were read from the hand-off and staged into this log. No automated action was taken on them in v1. A future M1L4 skill ("Memory Architecture") will act on these to generate CLAUDE.md and AGENTS.md tailored to the project's feature set.

## Next steps

Next: a future skill will set up agent context (CLAUDE.md, AGENTS.md). For now, your project is scaffolded and verified — happy hacking.

Useful manual steps in the meantime:
- `python manage.py migrate` to apply the initial Django migrations (fresh `db.sqlite3` — the old one was removed before this run).
- `python manage.py createsuperuser` to create the first admin user (has_auth = true).
- Review the scaffolded `no_bias_essay_grader/settings.py` — update SECRET_KEY, ALLOWED_HOSTS, and DATABASE for your environment before deploying.
- Upgrade Django to 6.0.8+ (or 5.2.17+) and sqlparse to 0.6.0+ to clear the 14 MODERATE advisories above — none are currently reachable by this project's code, but both are one `uv pip install --upgrade` away from clean.
- `git add`/commit the regenerated scaffold files if you want this run's state (fresh SECRET_KEY, fresh db.sqlite3) checked in over the prior commit's version.
