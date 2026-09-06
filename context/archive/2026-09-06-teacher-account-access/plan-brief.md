# Teacher Account Access — Plan Brief

> Full plan: `context/changes/teacher-account-access/plan.md`

## What & Why

Roadmap Slice S-01 asks for teacher registration, login, and logout (PRD FR-001/002/003). This capability already exists — it was built earlier in this session as the `accounts/` Django app. This plan formalizes that work into a tracked change so it can move through the pipeline (`/10x-implement` → `/10x-archive`) and close S-01 in the roadmap.

## Starting Point

`accounts/` already implements the full flow: registration (email + password, auto-login on success), email-based login, logout, and a login-required panel. 5 tests in `accounts/tests.py` cover it and currently pass.

## Desired End State

FR-001/002/003 are confirmed satisfied against the actual code, with no gaps. S-01 can then progress to `done` once this change is implemented (trivially — no code to write) and archived.

## Key Decisions Made

| Decision                                  | Choice                                       | Why (1 sentence)                                                    | Source |
| ------------------------------------------ | --------------------------------------------- | --------------------------------------------------------------------- | ------ |
| Scope of this plan                         | Verification only, no new code                | The feature is already built and tested — writing new code would be redundant. | Plan   |
| Number of phases                           | 1                                              | Nothing to design or sequence — just confirm and record.              | Plan   |

## Scope

**In scope:** Verifying `accounts/` against FR-001/FR-002/FR-003 and the US-01 login precondition; re-running the existing test suite as evidence.

**Out of scope:** Any new code in `accounts/`; password reset/OAuth; admin/director roles; `grading/` (separate change, roadmap Slice S-02).

## Architecture / Approach

No architecture change. This plan re-reads the existing `accounts/forms.py`, `views.py`, `urls.py`, and `tests.py`, and checks each PRD acceptance point against them.

## Phases at a Glance

| Phase                              | What it delivers                                    | Key risk                              |
| ----------------------------------- | ----------------------------------------------------- | ---------------------------------------- |
| 1. Verify existing implementation  | Documented confirmation that FR-001/002/003 hold      | None — feature already tested and working |

**Prerequisites:** None — `accounts/` already exists.
**Estimated effort:** One short session; no code changes.

## Open Risks & Assumptions

- Assumes no PRD or scope changes to teacher account access since `accounts/` was built earlier this session.

## Success Criteria (Summary)

- `python manage.py test accounts` and `python manage.py check` both pass.
- FR-001/002/003 are each traced to the code path that satisfies them.
