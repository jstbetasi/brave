---
project: Aplikacja webowa oceniająca eseje wg szkolnej skali ocen
context_type: greenfield
updated: 2026-05-24

checkpoint:
  current_phase: 8
  phases_completed: [1, 2, 3, 4, 5, 6, 7]
  frs_drafted: 6
  quality_check_status: accepted
  timeline_budget:
    mvp_weeks: 3
    after_hours_only: true
    hard_deadline: null
product_type: web-app
target_scale:
  users: small
---

## Vision & Problem Statement

Nauczyciel szkolny sprawdzający dużą partię esejów traci czas i — co ważniejsze — nieświadomie dryfuje w kryteriach oceniania: ta sama praca mogłaby dostać inną ocenę zależnie od kolejności sprawdzania, zmęczenia czy nastroju. To systemowa niesprawiedliwość, nie błąd ludzki do wyeliminowania samą dobrą wolą.

Kluczowy insight: LLM jest lepszym asystentem oceniania nie dlatego, że jest szybszy, ale dlatego, że nie ma osobistych doświadczeń zakłócających ocenę. Ocenia **aspekty jakości pisania** (struktura, argumentacja, spójność, język, styl) bez weryfikacji prawdziwości tez zawartych w eseju — dokładnie tak, jak powinien działać sprawiedliwy system oceniania formy.

Aplikacja ma dać nauczycielowi szkolnemu narzędzie do spójnego, transparentnego oceniania esejów wg zdefiniowanej skali, z uzasadnieniem każdej oceny.

## User & Persona

**Persona główna: Nauczyciel szkolny**
- Rola: nauczyciel języka polskiego, historii lub innego przedmiotu humanistycznego w podstawówce lub liceum
- Kontekst pracy: sprawdza prace całej klasy (20–35 esejów) naraz, często wieczorami lub w weekend
- Cel: wystawić sprawiedliwe, uzasadnione oceny zgodne ze szkolną skalą
- Frustracja: po sprawdzeniu 15. eseju z rzędu kryteria rozjeżdżają się niepostrzeżenie

## Access Control

- Model: login email + hasło (OAuth jako opcja późniejsza)
- Wielu nauczycieli na jednej instancji — model płaski: każdy nauczyciel widzi wyłącznie swoje sesje oceniania i wyniki
- Brak ról administracyjnych w MVP (dyrektor/admin szkoły — poza zakresem)
- Rejestracja: samodzielna (email + hasło) lub zaproszenie — do decyzji w stack-selector

## Success Criteria

### Primary
Nauczyciel wkleja tekst eseju, klika "oceń" i widzi ocenę końcową w skali 1–6 wraz z wynikami w 4 kategoriach (forma, argumentacja, język, struktura) — obliczoną wg wbudowanej, stałej rubryki. Przepływ działa od logowania do wyniku bez błędów.

### Secondary
Eksport do CSV zawierający: ocenę końcową, wyniki per kategoria, uzasadnienie LLM dla każdej kategorii oraz zastosowaną regułę oceniania (rubryke). Nauczyciel może pobrać plik z wynikami sesji.

### Guardrails
- Dane nauczycieli są izolowane: nauczyciel A nigdy nie widzi esejów ani wyników nauczyciela B
- Treść eseju nie jest przechowywana permanentnie — idzie do LLM i nie jest zapisywana po zakończeniu sesji (prywatność ucznia / RODO)
- Wynik jest zawsze w skali 1–6: aplikacja nigdy nie zwraca NULL ani surowego błędu zamiast oceny; LLM-failures są obsługiwane po stronie aplikacji

## Functional Requirements

### Konto
- FR-001: Nauczyciel może zarejestrować konto (email + hasło). Priority: must-have
  > Socrates: Kontrargument rozważony: brak kontrargumentu — konto jest fundamentem izolacji danych między nauczycielami (guardrail). Pozostaje bez zmian.
- FR-002: Nauczyciel może zalogować się do aplikacji. Priority: must-have
  > Socrates: j.w. — auth jest konieczny. Pozostaje bez zmian.
- FR-003: Nauczyciel może wylogować się. Priority: must-have
  > Socrates: j.w. Pozostaje bez zmian.

### Ocenianie
- FR-004: Nauczyciel może wkleić tekst eseju, nadać mu etykietę autora (pole opcjonalne z placeholderem „np. Jan Kowalski"; jeśli puste — fallback do daty i czasu jako nazwy pliku CSV) i zlecić ocenianie. Priority: must-have
  > Socrates: Kontrargument zaakceptowany: data i czas jako domyślna wartość pola jest myląca przy ocenianiu 30 prac. Korekta: pole jest puste z placeholderem zamiast pre-filled datą — fallback do daty i czasu używany tylko jako nazwa pliku gdy pole pozostanie puste.
- FR-005: Nauczyciel może zobaczyć wynik oceniania: ocenę końcową w skali 1–6, wynik per kategoria (forma / argumentacja / język / struktura) oraz uzasadnienie LLM dla każdej kategorii. Priority: must-have
  > Socrates: Kontrargument rozważony: brak — to jest sedno produktu. Pozostaje bez zmian.

### Eksport
- FR-006: Nauczyciel może wyeksportować wynik bieżącego eseju do CSV; nazwa pliku pochodzi z etykiety autora (fallback: data i czas). Priority: nice-to-have
  > Socrates: Kontrargument rozważony: brak — eksport jest niezbędny do użytku w dzienniku. Pozostaje bez zmian.

## User Stories

### US-01: Ocenianie eseju
- Given: nauczyciel jest zalogowany, widzi pole tekstu eseju oraz puste pole "autor" z placeholderem „np. Jan Kowalski"
- When: wkleja tekst eseju, opcjonalnie zmienia etykietę autora i klika "oceń"
- Then: widzi ocenę końcową w skali 1–6, wynik w 4 kategoriach (forma / argumentacja / język / struktura) oraz uzasadnienie LLM dla każdej kategorii; eksport CSV pobiera plik o nazwie [autor].csv

## Business Logic

Aplikacja klasyfikuje esej w 4 kategoriach jakości pisania (forma, język, struktura, argumentacja) bez oceny tez — eliminując uprzedzenia nauczyciela z etapu przyznawania etykiet — a następnie wylicza ocenę końcową wg stałych wag.

Arkusz kalkulacyjny mógłby wyliczyć ocenę z gotowych etykiet, ale **przyznanie etykiet** jest tym, co wymaga bezstronności. LLM podejmuje tę decyzję zamiast nauczyciela, ponieważ nie zna autora, nie jest zmęczony i nie ma opinii na temat prawdziwości tez.

Dostępne etykiety per kategoria (wbudowana, stała rubryka w MVP):
- Forma: Dobra / Słaba/ Zła
- Argumentacja: Dobra / Słaba / Zła
- Język: Bogaty / Dobry / Słaby / Zły
- Struktura: Dobra / Słaba / Zła

| Kategoria | Etykieta | Punkty |
|---|---|---|
| Forma | Dobra | 2 |
| Forma | Słaba | 1 |
| Forma | Zła | 0 |
| Argumentacja | Dobra | 2 |
| Argumentacja | Słaba | 1 |
| Argumentacja | Zła | 0 |
| Język | Bogaty | 3 |
| Język | Dobry | 2 |
| Język | Słaby | 1 |
| Język | Zły | 0 |
| Struktura | Dobra | 2 |
| Struktura | Słaba | 1 |
| Struktura | Zła | 0 |

Max 9 punktów. 0 punktów w jakiejkolwiek kategorii skutkuje oceną 1.
Podział sumy punktów na oceny: 9→6, 8→5, 6-7→4, 5→3, 4→2

Ocena końcowa 1–6 jest wynikiem mechanicznego przeliczenia etykiet na punkty wg stałych wag, a następnie mapowania sumy punktów na przedziały ocen. Wagi i przedziały są wbudowane w aplikację (niezmienne w v1).

## Non-Functional Requirements

- Czas odpowiedzi: nauczyciel otrzymuje wynik oceniania w ciągu 30 sekund od kliknięcia „oceń" (dotyczy pojedynczego eseju)
- Prywatność: treść eseju nie jest dostępna w systemie po zakończeniu oceniania — nie jest zapisywana permanentnie; dane ucznia chronione zgodnie z RODO
- Dostępność: aplikacja działa w nowoczesnej przeglądarce bez instalowania oprogramowania
- Język: cały interfejs i wszystkie komunikaty błędów wyświetlane po polsku

## Non-Goals

- Ocenianie treści merytorycznej (prawdziwość tez) — aplikacja nigdy nie weryfikuje czy tezy zawarte w eseju są prawdziwe; ocenia wyłącznie formę pisania
- Integracja z dziennikiem elektronicznym (Librus, Synergia i inne) — eksport CSV wystarczy na v1; integracja z zewnętrznymi systemami szkolnymi poza zakresem
- Panel administratora szkoły / widok zbiorczy nauczycieli — dyrektor lub admin widzi wyniki wszystkich nauczycieli; płaski model bez ról w MVP
- Edycja rubryki (wagi kategorii + progi ocen skali 1–6) — wbudowana stała rubryka w MVP; konfigurowalność odłożona do v2 (decyzja scope-down z Fazy 3)

## Open Questions

<!-- Zbierane na bieżąco -->
