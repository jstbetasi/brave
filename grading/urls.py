from django.urls import path

from . import views

urlpatterns = [
    path("", views.GradeEssayView.as_view(), name="ocen"),
    path("<int:pk>/", views.ResultView.as_view(), name="wynik"),
    path("<int:pk>/eksport.csv", views.ExportCsvView.as_view(), name="eksport_csv"),
]
