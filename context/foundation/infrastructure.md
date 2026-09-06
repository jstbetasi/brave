---
project: no-bias-essay-grader
researched_at: 2026-09-06
recommended_platform: self-hosted (own server)
runner_up: n/a
context_type: mvp
tech_stack:
  language: python
  framework: django
  runtime: uv
---

## Recommendation

**Deploy to the user's own web server (self-hosted).**

The deployment target was already decided by the user before this research ran — they own and operate their own server. This is not a decision produced by `/10x-infra-research`'s scored platform comparison; the six-candidate pool this skill normally evaluates (Cloudflare, Vercel, Netlify, Fly.io, Railway, Render) was not researched or scored, because the platform choice isn't among them. `context/foundation/tech-stack.md` had recorded `deployment_target: fly` as a starter-registry default hint — that hint is now superseded by this decision.

## Platform Comparison

Not applicable. No managed-platform research or scoring was run for this decision — see Out of Scope.

## Anti-Bias Cross-Check

Not applicable — the three cross-check lenses (devil's advocate, pre-mortem, unknown unknowns) are designed to stress-test a *recommendation this skill produced*. They weren't run here since there was no candidate to stress-test; the decision is the user's own infrastructure. If useful, the risk register below captures self-hosting-specific risks from first principles instead.

## Operational Story

Server: Ubuntu, nginx (reverse proxy + TLS termination) → gunicorn (WSGI) → Django. Deploy via `git pull`.

- **Preview deploys**: Not set up — single environment (production) on this server. A PR/branch preview would need a second nginx server block + gunicorn instance on a different port/socket; out of scope until there's a concrete need.
- **Secrets**: Not yet wired (see the `SECRET_KEY`/`DEBUG` hardcoding already flagged in `context/foundation/health-check.md`). Recommended: an `.env` file outside git (`/etc/no-bias-essay-grader/.env` or similar, root-readable only), loaded by `django-environ`, and referenced from the gunicorn systemd unit via `EnvironmentFile=`. Rotation = edit the file + `systemctl restart gunicorn`.
- **Rollback**: `git checkout <previous-commit-or-tag>` followed by a gunicorn restart. **Caveat**: Django migrations do not auto-rollback — if the bad deploy included a migration, `git checkout` alone leaves the schema ahead of the code. Any deploy that includes a migration needs a known-good rollback migration path (or a pre-deploy DB backup) before it ships, not improvised after the fact.
- **Approval**: Redeploy, gunicorn restart, and `migrate` should stay human-approved steps until there's a single scripted deploy command that's been proven idempotent — this server has no platform-level safety net (no automatic health check, no managed rollback) the way Fly.io/Railway would provide.
- **Logs**: `journalctl -u gunicorn` (app/WSGI errors) and `/var/log/nginx/access.log` + `/var/log/nginx/error.log` (request-level). Both are readable read-only via SSH without a dashboard — agent-operable once SSH access is granted.

## Risk Register

| Risk | Source | Likelihood | Impact | Mitigation |
|---|---|---|---|---|
| No managed TLS/health-check/auto-restart — self-hosted servers don't provide the automatic recovery a PaaS would | Research finding | M | H | Run gunicorn under a systemd unit with `Restart=on-failure`; renew TLS via certbot's cron/systemd timer |
| `git pull` deploys don't roll back database migrations | Research finding | M | H | Treat any deploy that includes a migration as higher-risk: take a DB backup first, and know the down-migration (or accept forward-fix-only) before deploying |
| Deploy was manual (`git pull` run by hand) — now scripted (see `deploy/deploy.sh`) | Research finding | L | M | Resolved — `deploy/deploy.sh` wraps `git pull` + `uv pip install -r requirements.txt` + `migrate` + `collectstatic` + `systemctl restart` into one deterministic command |
| `SECRET_KEY`/`DEBUG=True` are still hardcoded in `settings.py` (flagged separately in `context/foundation/health-check.md`) | Research finding | H | H | Externalize to environment variables before this server goes live in production |
| No CI/CD pipeline currently wired to this server (confirmed in health-check.md) | Research finding | H | M | Out of scope for this file — GitHub Actions auto-deploy-on-merge is the intended flow per `tech-stack.md`, still to be wired to this server |

## Getting Started

The deploy artifacts described below are now in the repo under `deploy/` (`no-bias-essay-grader.service`, `nginx.conf`, `deploy.sh`), and `settings.py` now reads `DJANGO_SECRET_KEY` / `DJANGO_DEBUG` / `DJANGO_ALLOWED_HOSTS` from the environment (via `django-environ`), falling back to the local-dev defaults when unset. Remaining steps to actually stand this up on the server:

1. Confirm the server has Python 3.12+ and `uv` installed (matching the local `.venv`); install if missing.
2. Clone the repo to `/srv/no-bias-essay-grader`, create `.venv`, and run `uv pip install -r requirements.txt`.
3. Create `/srv/no-bias-essay-grader/.env` from `.env.example`, with a real `DJANGO_SECRET_KEY`, `DJANGO_DEBUG=False`, and the server's actual `DJANGO_ALLOWED_HOSTS`.
4. Install `deploy/no-bias-essay-grader.service` to `/etc/systemd/system/`, `systemctl daemon-reload`, `systemctl enable --now no-bias-essay-grader`.
5. Install `deploy/nginx.conf` to `/etc/nginx/sites-available/`, symlink into `sites-enabled`, update `server_name`, then run certbot for TLS.
6. From then on, deploy via `./deploy/deploy.sh` (requires passwordless `sudo systemctl restart no-bias-essay-grader` for the deploying user, or run the last line manually).
7. Confirm `journalctl -u no-bias-essay-grader` and the nginx log paths are reachable via SSH before the first real deploy.

## Out of Scope

The following were not evaluated in this research:
- Comparison against Cloudflare / Vercel / Netlify / Fly.io / Railway / Render — the user's own server was already the decided target, so the platform-comparison step of `/10x-infra-research` was skipped.
- Docker image configuration
- CI/CD pipeline setup
- Production-scale architecture (multi-region, HA, DR)
