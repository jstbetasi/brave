"""Wbudowana, stała rubryka oceniania eseju (patrz context/foundation/prd.md).

Ocenianie jest w pełni deterministyczne i mechaniczne — takie same dane
wejściowe zawsze dają taki sam wynik. Brak wywołań do modeli AI i brak
zależności od czynników losowych: to eliminuje dryf oceniania, o którym
mowa w PRD (zmęczenie, kolejność sprawdzania, nastrój oceniającego).
"""

import re
from dataclasses import dataclass

PUNKTY_ZA_ETYKIETE = {
    "forma": {"Dobra": 2, "Zła": 0},
    "argumentacja": {"Dobra": 2, "Do poprawy": 1, "Zła": 0},
    "jezyk": {"Bogaty": 3, "Dobry": 2, "Słaby": 1, "Zły": 0},
    "struktura": {"Dobra": 2, "Zła": 0},
}

# (minimalna suma punktów, ocena) — sprawdzane w kolejności malejącej.
PROGI_OCEN = [
    (9, 6),
    (7, 5),
    (5, 4),
    (3, 3),
    (1, 2),
    (0, 1),
]

ZNACZNIKI_ARGUMENTACYJNE = [
    "ponieważ", "dlatego", "zatem", "wobec tego", "z jednej strony",
    "z drugiej strony", "jednak", "jednakże", "natomiast", "co więcej",
    "ponadto", "na przykład", "przykładowo", "w rezultacie",
    "w konsekwencji", "podsumowując", "reasumując", "wnioskuję",
    "argument", "kontrargument", "teza",
]

_SLOWO = re.compile(r"[a-ząćęłńóśźż]+", re.IGNORECASE)


def _slowa(tekst: str) -> list[str]:
    return _SLOWO.findall(tekst.lower())


def _akapity(tekst: str) -> list[str]:
    return [a for a in re.split(r"\n\s*\n", tekst) if a.strip()]


@dataclass(frozen=True)
class WynikKategorii:
    etykieta: str
    uzasadnienie: str


@dataclass(frozen=True)
class WynikOceniania:
    forma: WynikKategorii
    argumentacja: WynikKategorii
    jezyk: WynikKategorii
    struktura: WynikKategorii
    punkty: int
    ocena: int


def _ocen_forme(tekst: str, slowa: list[str]) -> WynikKategorii:
    oczyszczony = tekst.strip()
    liczba_slow = len(slowa)
    dlugosc_ok = 150 <= liczba_slow <= 1500
    zaczyna_wielka_litera = bool(oczyszczony) and oczyszczony[0].isupper()
    konczy_poprawnie = oczyszczony.endswith((".", "!", "?", '"', "”"))
    nie_same_wielkie = not oczyszczony.isupper()

    etykieta = (
        "Dobra"
        if dlugosc_ok and zaczyna_wielka_litera and konczy_poprawnie and nie_same_wielkie
        else "Zła"
    )
    uzasadnienie = (
        f"Tekst liczy {liczba_slow} słów "
        f"({'mieści się' if dlugosc_ok else 'nie mieści się'} w oczekiwanym zakresie 150–1500), "
        f"{'zaczyna się wielką literą' if zaczyna_wielka_litera else 'nie zaczyna się wielką literą'} "
        f"i {'kończy się znakiem kończącym zdanie' if konczy_poprawnie else 'nie kończy się znakiem kończącym zdanie'}."
    )
    return WynikKategorii(etykieta, uzasadnienie)


def _ocen_strukture(tekst: str) -> WynikKategorii:
    akapity = _akapity(tekst)
    pelne_akapity = [a for a in akapity if len(_slowa(a)) >= 15]
    etykieta = "Dobra" if len(pelne_akapity) >= 3 else "Zła"
    uzasadnienie = (
        f"Wykryto {len(pelne_akapity)} akapit(y/ów) o długości co najmniej 15 słów "
        "(wymagane: co najmniej 3, np. wstęp, rozwinięcie, zakończenie)."
    )
    return WynikKategorii(etykieta, uzasadnienie)


def _ocen_jezyk(slowa: list[str]) -> WynikKategorii:
    liczba_slow = len(slowa)
    if liczba_slow == 0:
        return WynikKategorii("Zły", "Brak treści do analizy słownictwa.")

    unikalne = len(set(slowa))
    wskaznik = unikalne / liczba_slow
    if wskaznik >= 0.6:
        etykieta = "Bogaty"
    elif wskaznik >= 0.45:
        etykieta = "Dobry"
    elif wskaznik >= 0.3:
        etykieta = "Słaby"
    else:
        etykieta = "Zły"
    uzasadnienie = (
        "Wskaźnik różnorodności słownictwa (liczba unikalnych słów / liczba wszystkich "
        f"słów) wynosi {wskaznik:.2f} ({unikalne}/{liczba_slow})."
    )
    return WynikKategorii(etykieta, uzasadnienie)


def _ocen_argumentacje(tekst: str) -> WynikKategorii:
    tekst_lower = tekst.lower()
    trafienia = [z for z in ZNACZNIKI_ARGUMENTACYJNE if z in tekst_lower]
    liczba = len(trafienia)
    if liczba >= 4:
        etykieta = "Dobra"
    elif liczba >= 2:
        etykieta = "Do poprawy"
    else:
        etykieta = "Zła"
    przyklady = ", ".join(trafienia[:3]) if trafienia else "brak"
    uzasadnienie = (
        f"Wykryto {liczba} znacznik(i/ów) argumentacyjnych w tekście (np. {przyklady})."
    )
    return WynikKategorii(etykieta, uzasadnienie)


def _oblicz_ocene(punkty: int) -> int:
    for prog, ocena in PROGI_OCEN:
        if punkty >= prog:
            return ocena
    return 1


def ocen_esej(tekst: str) -> WynikOceniania:
    tekst = tekst or ""
    slowa = _slowa(tekst)

    forma = _ocen_forme(tekst, slowa)
    argumentacja = _ocen_argumentacje(tekst)
    jezyk = _ocen_jezyk(slowa)
    struktura = _ocen_strukture(tekst)

    punkty = (
        PUNKTY_ZA_ETYKIETE["forma"][forma.etykieta]
        + PUNKTY_ZA_ETYKIETE["argumentacja"][argumentacja.etykieta]
        + PUNKTY_ZA_ETYKIETE["jezyk"][jezyk.etykieta]
        + PUNKTY_ZA_ETYKIETE["struktura"][struktura.etykieta]
    )
    ocena = _oblicz_ocene(punkty)

    return WynikOceniania(forma, argumentacja, jezyk, struktura, punkty, ocena)
