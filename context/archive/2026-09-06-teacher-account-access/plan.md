# Teacher Account Access Implementation Plan

## Overview

Formalize the already-implemented teacher account access (registration, login, logout) into a tracked change, verifying the existing `accounts/` implementation against PRD FR-001/FR-002/FR-003 and closing the loop so roadmap Slice S-01 (`context/foundation/roadmap.md`) can progress through the pipeline to `done`. No new code is written by this plan — it verifies and documents.

## Current State Analysis

The `accounts/` Django app already implements the full flow:

- `accounts/forms.py` — `RegisterForm` (email + password, enforces email uniqueness, sets `username = email`), `EmailAuthenticationForm` (relabels login's username field as "Email")
- `accounts/views.py` — `RegisterView` (auto-logs in on signup), `PanelView` (login-required)
- `accounts/urls.py` — `/konto/rejestracja/`, `/konto/logowanie/`, `/konto/wyloguj/`; project `urls.py` wires `/panel/`
- Templates: `accounts/templates/accounts/register.html`, `.../panel.html`, `.../registration/login.html`
- `accounts/tests.py` — 5 tests, currently passing

No gaps were found between the PRD requirements and the existing code.

## Desired End State

FR-001, FR-002, and FR-003 are confirmed satisfied by the existing `accounts/` code, with the check documented in this plan. Roadmap Slice S-01 can then move to `in-progress` (via `/10x-implement`) and, once archived, to `done`.

### Key Discoveries:

- `accounts/forms.py` — `RegisterForm.clean_email` enforces uniqueness; `save()` sets `username = email` (flat auth model, no separate username per AGENTS.md guardrail)
- `accounts/views.py` — `RegisterView.form_valid` calls `login()` immediately after registration (matches PRD: registration flows straight into a usable session)
- `accounts/urls.py` — route names (`register`, `login`, `logout`, `panel`) are flat, no namespace — matches the project's existing URL convention
- `accounts/tests.py` — covers: register creates user + auto-login, duplicate email rejected, email-based login, `panel` requires login (redirects with `?next=`), logout redirects to login

## What We're NOT Doing

- No new code changes to `accounts/`
- No password reset flow or OAuth (PRD explicitly defers OAuth to a future version)
- No admin/director role or cross-teacher view (PRD Non-Goals — flat model only)
- No changes to `grading/` (that's roadmap Slice S-02, a separate change)

## Implementation Approach

Single verification phase: re-run the existing automated test suite as evidence, then manually cross-check each FR-001/002/003 acceptance point and the US-01 login precondition against the actual code paths, recording the result inline in this plan's Success Criteria.

## Phase 1: Verify existing implementation against FR-001/002/003

### Overview

Confirm the already-built `accounts/` app satisfies every acceptance point the PRD attaches to teacher account access, with no code changes.

### Changes Required:

#### 1. Verification pass (no file changes)

**File**: `accounts/` (read-only verification, no modification)

**Intent**: Confirm each acceptance criterion from PRD FR-001/FR-002/FR-003 and the US-01 login precondition ("Given nauczyciel jest zalogowany") is satisfied by the current code, with the automated test suite as evidence.

**Contract**: No interface changes. Verification target is the existing contract: `RegisterForm.Meta.fields = ("email",)`, `EmailAuthenticationForm.username` as an `EmailField`, and URL names `register` / `login` / `logout` / `panel`.

### Success Criteria:

#### Automated Verification:

- Accounts test suite passes: `python manage.py test accounts`
- Full Django system check passes: `python manage.py check`

#### Manual Verification:

- FR-001 confirmed: a new teacher can register an account with email + password
- FR-002 confirmed: a registered teacher can log in
- FR-003 confirmed: a logged-in teacher can log out
- Data-isolation guardrail confirmed structurally: no grading result is reachable without an authenticated session (`LoginRequiredMixin` gates `PanelView` and the `grading` views)

**Implementation Note**: After completing this phase and all automated verification passes, pause here for manual confirmation from the human that the manual testing was successful before proceeding to the next phase.

---

## Testing Strategy

### Unit Tests:

- Already covered by the existing 5 tests in `accounts/tests.py` — no new tests needed.

### Integration Tests:

- Not applicable beyond the existing Django test-client coverage in `accounts/tests.py`.

### Manual Testing Steps:

1. Register a throwaway account via `/konto/rejestracja/`; confirm redirect to `/panel/` with auto-login.
2. Log out via `/konto/wyloguj/`.
3. Log back in via `/konto/logowanie/` with the same email + password.
4. Confirm `/panel/` redirects to `/konto/logowanie/?next=/panel/` when logged out.

## Performance Considerations

Not applicable — no changes.

## Migration Notes

Not applicable — no schema changes.

## References

- Roadmap: `context/foundation/roadmap.md` (Slice S-01)
- PRD: `context/foundation/prd.md` (FR-001, FR-002, FR-003, US-01)
- Existing implementation: `accounts/forms.py`, `accounts/views.py`, `accounts/urls.py`, `accounts/tests.py`

## Progress

> Convention: `- [ ]` pending, `- [x]` done. Append ` — <commit sha>` when a step lands. Do not rename step titles. See `references/progress-format.md`.

### Phase 1: Verify existing implementation against FR-001/002/003

#### Automated

- [x] 1.1 Accounts test suite passes: `python manage.py test accounts` — 357d0a1
- [x] 1.2 Full Django system check passes: `python manage.py check` — 357d0a1

#### Manual

- [x] 1.3 FR-001 confirmed: register with email + password — 357d0a1
- [x] 1.4 FR-002 confirmed: log in — 357d0a1
- [x] 1.5 FR-003 confirmed: log out — 357d0a1
- [x] 1.6 Data-isolation guardrail confirmed structurally (login required before any grading result is reachable) — 357d0a1
