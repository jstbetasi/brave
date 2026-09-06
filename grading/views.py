import csv

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.text import slugify
from django.views import View
from django.views.generic import DetailView

from .forms import EssayForm
from .models import GradingResult
from .rubric import ocen_esej


class GradeEssayView(LoginRequiredMixin, View):
    template_name = "grading/ocen.html"

    def get(self, request):
        return render(request, self.template_name, {"form": EssayForm()})

    def post(self, request):
        form = EssayForm(request.POST)
        if not form.is_valid():
            return render(request, self.template_name, {"form": form})

        wynik = ocen_esej(form.cleaned_data["tekst"])
        result = GradingResult.objects.create(
            nauczyciel=request.user,
            autor=form.cleaned_data["autor"],
            forma=wynik.forma.etykieta,
            forma_uzasadnienie=wynik.forma.uzasadnienie,
            argumentacja=wynik.argumentacja.etykieta,
            argumentacja_uzasadnienie=wynik.argumentacja.uzasadnienie,
            jezyk=wynik.jezyk.etykieta,
            jezyk_uzasadnienie=wynik.jezyk.uzasadnienie,
            struktura=wynik.struktura.etykieta,
            struktura_uzasadnienie=wynik.struktura.uzasadnienie,
            punkty=wynik.punkty,
            ocena=wynik.ocena,
        )
        return redirect("wynik", pk=result.pk)


class ResultView(LoginRequiredMixin, DetailView):
    template_name = "grading/wynik.html"
    context_object_name = "wynik"
    model = GradingResult

    def get_queryset(self):
        return GradingResult.objects.filter(nauczyciel=self.request.user)


class ExportCsvView(LoginRequiredMixin, View):
    def get(self, request, pk):
        wynik = get_object_or_404(GradingResult, pk=pk, nauczyciel=request.user)
        nazwa = slugify(wynik.autor) or wynik.utworzono.strftime("%Y%m%d_%H%M%S")

        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = f'attachment; filename="{nazwa}.csv"'

        writer = csv.writer(response)
        writer.writerow(["Kategoria", "Ocena", "Uzasadnienie"])
        writer.writerow(["Forma", wynik.forma, wynik.forma_uzasadnienie])
        writer.writerow(["Argumentacja", wynik.argumentacja, wynik.argumentacja_uzasadnienie])
        writer.writerow(["Język", wynik.jezyk, wynik.jezyk_uzasadnienie])
        writer.writerow(["Struktura", wynik.struktura, wynik.struktura_uzasadnienie])
        writer.writerow([])
        writer.writerow(["Ocena końcowa", wynik.ocena])
        writer.writerow(["Suma punktów", f"{wynik.punkty}/9"])
        return response
