from django.conf import settings
from django.db import models


class GradingResult(models.Model):
    """Wynik oceniania jednego eseju.

    Treść eseju nigdy nie jest tu przechowywana (RODO) — tylko wynik
    obliczony przez rubrykę (grading.rubric) i metadane.
    """

    nauczyciel = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="wyniki_oceniania"
    )
    autor = models.CharField(max_length=255, blank=True)

    forma = models.CharField(max_length=20)
    forma_uzasadnienie = models.TextField()
    argumentacja = models.CharField(max_length=20)
    argumentacja_uzasadnienie = models.TextField()
    jezyk = models.CharField(max_length=20)
    jezyk_uzasadnienie = models.TextField()
    struktura = models.CharField(max_length=20)
    struktura_uzasadnienie = models.TextField()

    punkty = models.PositiveSmallIntegerField()
    ocena = models.PositiveSmallIntegerField()

    utworzono = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-utworzono"]

    def __str__(self):
        etykieta = self.autor or self.utworzono.strftime("%Y-%m-%d %H:%M")
        return f"{etykieta} — ocena {self.ocena}"
