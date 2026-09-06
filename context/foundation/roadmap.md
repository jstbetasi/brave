---
project: Aplikacja webowa oceniająca eseje wg szkolnej skali ocen
version: 1
status: draft
created: 2026-09-06
updated: 2026-09-06
prd_version: 1
main_goal: speed
top_blocker: capacity
milestone_id: ship-mvp-to-production
milestone_seq: 1
milestone_status: open
---

# Roadmap: Aplikacja webowa oceniająca eseje wg szkolnej skali ocen

> Derived from `context/foundation/prd.md` (v1) + auto-researched codebase baseline.
> Edit-in-place; archive when superseded.
> Slices below are listed in dependency order. The "At a glance" table is the index.

## Milestone

**M-1: Wystawienie gotowego MVP na produkcję** — Status: open

- **Intent:** Rdzeń produktu (konto nauczyciela, bezstronne ocenianie esejów, eksport CSV) jest już zaimplementowany i przetestowany. Ten milestone domyka pętlę: doprowadzić to, co już działa lokalnie, do stanu dostępnego dla realnych nauczycieli na własnym serwerze użytkownika.
- **Source materials:** `context/foundation/prd.md` (v1)
- **Done when:** F-01, S-01 i S-02 poniżej mają status `done`.

## Vision recap

Nauczyciel sprawdzający dużą partię esejów nieświadomie dryfuje w kryteriach oceniania — ta sama praca mogłaby dostać inną ocenę zależnie od kolejności sprawdzania, zmęczenia czy nastroju. Automatyczna, mechaniczna klasyfikacja jakości pisania (forma, argumentacja, język, struktura) — bez oceny prawdziwości tez — eliminuje ten dryf, ponieważ nie ma osobistych doświadczeń zakłócających ocenę.

## North star

**S-02: Nauczyciel ocenia esej i widzi wynik** — to jest przepływ opisany dosłownie jako Kryterium sukcesu (Primary) w PRD; jego pomyślne dostarczenie dowodzi, że eliminacja stronniczości w ocenianiu faktycznie działa.

> "Gwiazda przewodnia" (north star) oznacza tu: najmniejszy kompletny przepływ, którego udane dostarczenie dowodzi, że produkt spełnia swoją podstawową obietnicę — umieszczony najwcześniej, jak pozwalają na to zależności, bo cała reszta ma znaczenie tylko wtedy, gdy to działa.

## At a glance

| ID    | Change ID                       | Outcome (user can …)                                              | Prerequisites | PRD refs                    | Status   |
| ----- | -------------------------------- | ------------------------------------------------------------------ | -------------- | ---------------------------- | -------- |
| F-01  | `self-hosted-production-deploy` | (foundation) aplikacja dostępna publicznie z przeglądarki           | —               | NFR (Dostępność)             | ready    |
| S-01  | `teacher-account-access`        | nauczyciel zakłada konto, loguje się i wylogowuje                   | —               | FR-001, FR-002, FR-003        | in-progress |
| S-02  | `essay-grading-and-csv-export`  | nauczyciel ocenia esej, widzi wynik i eksportuje go do CSV          | S-01            | US-01, FR-004, FR-005, FR-006 | proposed |

## Baseline

What's already in place in the codebase as of `2026-09-06` (bezpośrednio zbadane w tej sesji — cały kod poniżej powstał w niej — i potwierdzone przez użytkownika).
Foundations below assume these are present and do NOT re-scaffold them.

- **Frontend:** present — szablony Django server-side pokrywają cały przepływ (rejestracja, logowanie, panel, ocenianie, wynik) — `accounts/templates/`, `grading/templates/`, `templates/base.html`. Bez stylowania CSS.
- **Backend / API:** present — `accounts/views.py`, `grading/views.py`, wpięte w `no_bias_essay_grader/urls.py`.
- **Data:** present — `grading/models.py:GradingResult`, migracja `0001_initial` zaaplikowana, SQLite.
- **Auth:** present — `accounts/` (rejestracja/logowanie/wylogowanie, model płaski email=username), 5 testów przechodzi.
- **Deploy / infra:** partial — `deploy/no-bias-essay-grader.service`, `deploy/nginx.conf`, `deploy/deploy.sh` gotowe w repo (ta sesja), `settings.py` czyta sekrety ze zmiennych środowiskowych; nic z tego nie jest jeszcze zainstalowane na realnym serwerze, brak CI/CD.
- **Observability:** absent — brak logowania błędów/monitoringu poza domyślnym Django.

## Foundations

### F-01: Wdrożenie produkcyjne na własnym serwerze

- **Outcome:** (foundation) aplikacja działa pod publicznym adresem, dostępna z przeglądarki bez lokalnej instalacji — nginx + gunicorn + systemd uruchomione na serwerze użytkownika, zgodnie z `context/foundation/infrastructure.md`.
- **Change ID:** `self-hosted-production-deploy`
- **PRD refs:** NFR (Dostępność: "aplikacja działa w nowoczesnej przeglądarce bez instalowania oprogramowania")
- **Unlocks:** realną weryfikację S-01 i S-02 przez prawdziwych użytkowników (nie tylko lokalny zestaw testów); domyka `Deploy/infra: partial` z Baseline
- **Prerequisites:** —
- **Parallel with:** S-01, S-02
- **Blockers:** —
- **Unknowns:**
  - Docelowa domena / adres serwera do wpisania w `nginx.conf` (`server_name`) i do certbota — Owner: user. Block: no (instalację można zacząć bez tego, domenę dopisać przed uruchomieniem TLS).
- **Risk:** Pozostałe kroki (SSH, systemd, nginx, TLS) są rutynowe i opisane w `infrastructure.md`, ale wymagają ręcznej pracy solo-developera po godzinach — stąd `top_blocker: capacity`, nie brak wiedzy czy decyzji.
- **Status:** ready

## Slices

### S-01: Nauczyciel zakłada konto, loguje się i wylogowuje

- **Outcome:** nauczyciel może zarejestrować konto (email + hasło), zalogować się i wylogować; dane każdego nauczyciela są izolowane od pozostałych (model płaski, bez ról).
- **Change ID:** `teacher-account-access`
- **PRD refs:** FR-001, FR-002, FR-003
- **Prerequisites:** —
- **Parallel with:** F-01
- **Blockers:** —
- **Unknowns:** —
- **Risk:** Już zaimplementowane i pokryte 5 testami (`accounts/tests.py`) w tej sesji — głównym ryzykiem jest regresja przy przyszłych zmianach bez ponownego uruchomienia zestawu testów.
- **Status:** in-progress

### S-02: Nauczyciel ocenia esej, widzi wynik i eksportuje go do CSV

- **Outcome:** nauczyciel wkleja tekst eseju, opcjonalnie nadaje etykietę autora, klika „oceń" i widzi ocenę końcową (1–6) wraz z wynikiem i uzasadnieniem w 4 kategoriach (forma / argumentacja / język / struktura); może pobrać wynik jako CSV.
- **Change ID:** `essay-grading-and-csv-export`
- **PRD refs:** US-01, FR-004, FR-005, FR-006
- **Prerequisites:** S-01 (wymaga zalogowanej sesji — `US-01` „Given nauczyciel jest zalogowany")
- **Parallel with:** F-01
- **Blockers:** —
- **Unknowns:** —
- **Risk:** Już zaimplementowane i pokryte 11 testami (`grading/tests.py`) w tej sesji, w tym izolacja danych między nauczycielami i brak trwałego zapisu treści eseju (RODO). Status pozostaje `proposed`, nie `ready`, dopóki S-01 formalnie nie przejdzie przez `/10x-plan` → `/10x-implement` → `/10x-archive` — patrz uwaga w podsumowaniu poniżej.
- **Status:** proposed

## Backlog Handoff

| Roadmap ID | Change ID                       | Suggested issue title                                    | Ready for `/10x-plan` | Notes |
| ---------- | -------------------------------- | ----------------------------------------------------------- | ---------------------- | ----- |
| F-01       | `self-hosted-production-deploy` | Wdroż aplikację na własnym serwerze (nginx + gunicorn)      | yes                    | Kod pomocniczy już w repo pod `deploy/` |
| S-01       | `teacher-account-access`        | Rejestracja, logowanie i wylogowanie nauczyciela             | yes                    | Już zaimplementowane w `accounts/` — formalizuje istniejący kod |
| S-02       | `essay-grading-and-csv-export`  | Ocenianie eseju z eksportem CSV                              | no                     | Stanie się `ready` po domknięciu S-01 w pipeline; kod już istnieje w `grading/` |

## Open Roadmap Questions

1. **Jaka jest docelowa domena / publiczny adres serwera dla wdrożenia?** — Owner: user. Block: F-01 (tylko krok TLS/`server_name`, nie start instalacji).

## Parked

- **Ocenianie treści merytorycznej (prawdziwość tez)** — Why parked: PRD §Poza zakresem — aplikacja nigdy nie weryfikuje, czy tezy zawarte w eseju są prawdziwe, ocenia wyłącznie formę pisania.
- **Integracja z dziennikiem elektronicznym (Librus, Synergia i inne)** — Why parked: PRD §Poza zakresem — eksport CSV wystarcza na v1.
- **Panel administratora szkoły / widok zbiorczy nauczycieli** — Why parked: PRD §Poza zakresem — płaski model bez ról w MVP.
- **Edycja rubryki (wagi kategorii + progi ocen)** — Why parked: PRD §Poza zakresem — wbudowana stała rubryka w MVP, konfigurowalność odłożona do v2.

## Milestone History

(brak — to pierwszy milestone)

## Done

(brak — `/10x-archive` uzupełni tę sekcję przy archiwizacji zmian pasujących do Change ID powyżej)
