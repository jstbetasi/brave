from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import GradingResult
from .rubric import ocen_esej

DOBRY_ESEJ = """
Wprowadzenie do tematu wymaga przedstawienia kilku istotnych kwestii, ponieważ
bez tego trudno zrozumieć dalszy wywód. Warto zaznaczyć, że temat ten budzi
wiele kontrowersji wśród badaczy zajmujących się tym zagadnieniem od lat.

Z jednej strony można argumentować, że rozwiązanie to przynosi korzyści
całemu społeczeństwu i warto je wdrażać na szeroką skalę. Z drugiej strony,
jednakże, pojawiają się głosy krytyczne wskazujące na istotne wady. Na
przykład wielu ekspertów podkreśla ryzyko związane z wdrożeniem takich
rozwiązań, co więcej wskazuje się na koszty społeczne tego procesu.

Podsumowując, należy uznać, że temat wymaga dalszej, pogłębionej analizy.
W konsekwencji warto rozważyć różne scenariusze i argumenty przedstawione
powyżej, zanim wyciągnie się ostateczne wnioski na temat tego zagadnienia.
""".strip()


class RubricTests(TestCase):
    def test_dobry_esej_dostaje_wysoka_ocene(self):
        wynik = ocen_esej(DOBRY_ESEJ)
        self.assertEqual(wynik.struktura.etykieta, "Dobra")
        self.assertEqual(wynik.argumentacja.etykieta, "Dobra")
        self.assertGreaterEqual(wynik.ocena, 4)

    def test_pusty_tekst_nie_powoduje_bledu(self):
        wynik = ocen_esej("")
        self.assertEqual(wynik.ocena, 1)
        self.assertEqual(wynik.punkty, 0)
        self.assertEqual(wynik.jezyk.etykieta, "Zły")

    def test_ocena_zawsze_w_zakresie_1_6(self):
        for tekst in ["", "a", DOBRY_ESEJ, "A" * 5000, "!!! ??? ..."]:
            wynik = ocen_esej(tekst)
            self.assertIn(wynik.ocena, range(1, 7))

    def test_deterministyczne_dla_tego_samego_wejscia(self):
        self.assertEqual(ocen_esej(DOBRY_ESEJ), ocen_esej(DOBRY_ESEJ))


class GradingFlowTests(TestCase):
    def setUp(self):
        self.teacher = User.objects.create_user(
            username="t1@example.com", email="t1@example.com", password="hasloTest123"
        )
        self.other_teacher = User.objects.create_user(
            username="t2@example.com", email="t2@example.com", password="hasloTest123"
        )
        self.client.login(username="t1@example.com", password="hasloTest123")

    def test_grading_requires_login(self):
        self.client.logout()
        response = self.client.get(reverse("ocen"))
        self.assertEqual(response.status_code, 302)

    def test_submitting_essay_creates_result_without_storing_text(self):
        response = self.client.post(reverse("ocen"), {"autor": "Jan Kowalski", "tekst": DOBRY_ESEJ})
        result = GradingResult.objects.get()
        self.assertRedirects(response, reverse("wynik", args=[result.pk]))
        self.assertEqual(result.nauczyciel, self.teacher)
        self.assertNotIn("tekst", [f.name for f in GradingResult._meta.get_fields()])

    def test_empty_essay_is_rejected_by_form(self):
        response = self.client.post(reverse("ocen"), {"autor": "", "tekst": "   "})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(GradingResult.objects.count(), 0)

    def test_teacher_cannot_see_other_teachers_result(self):
        self.client.post(reverse("ocen"), {"autor": "", "tekst": DOBRY_ESEJ})
        result = GradingResult.objects.get()
        self.client.logout()
        self.client.login(username="t2@example.com", password="hasloTest123")
        response = self.client.get(reverse("wynik", args=[result.pk]))
        self.assertEqual(response.status_code, 404)

    def test_teacher_cannot_export_other_teachers_result(self):
        self.client.post(reverse("ocen"), {"autor": "", "tekst": DOBRY_ESEJ})
        result = GradingResult.objects.get()
        self.client.logout()
        self.client.login(username="t2@example.com", password="hasloTest123")
        response = self.client.get(reverse("eksport_csv", args=[result.pk]))
        self.assertEqual(response.status_code, 404)

    def test_csv_export_filename_uses_author(self):
        self.client.post(reverse("ocen"), {"autor": "Jan Kowalski", "tekst": DOBRY_ESEJ})
        result = GradingResult.objects.get()
        response = self.client.get(reverse("eksport_csv", args=[result.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertIn("jan-kowalski.csv", response["Content-Disposition"])
        self.assertEqual(response["Content-Type"], "text/csv")

    def test_csv_export_filename_falls_back_to_timestamp(self):
        self.client.post(reverse("ocen"), {"autor": "", "tekst": DOBRY_ESEJ})
        result = GradingResult.objects.get()
        response = self.client.get(reverse("eksport_csv", args=[result.pk]))
        oczekiwana = result.utworzono.strftime("%Y%m%d_%H%M%S")
        self.assertIn(f"{oczekiwana}.csv", response["Content-Disposition"])
