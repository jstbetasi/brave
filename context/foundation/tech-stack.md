---
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
---

## Why this stack

Django is the recommended default for `(web-app, python)` and a clean fit for a 3-week, after-hours MVP with small-scale users. It ships auth, ORM, admin, and migrations out of the box — every structural need in the PRD is covered without third-party additions. Auth (FR-001–003: register, login, logout) maps directly to `django.contrib.auth`; no external auth library needed for MVP. The short timeline and after-hours constraint favor a batteries-included stack with verified bootstrapper confidence to eliminate setup overhead. Fly.io is the starter's default deployment target; GitHub Actions with auto-deploy-on-merge matches solo-developer discipline. The `typed: false` flag on the Django card is a known gap — addressable with `django-stubs` + `mypy` and a CLAUDE.md annotation if typed-agent coverage becomes a priority.
