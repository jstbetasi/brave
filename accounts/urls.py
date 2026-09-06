from django.contrib.auth import views as auth_views
from django.urls import path

from . import views
from .forms import EmailAuthenticationForm

urlpatterns = [
    path("rejestracja/", views.RegisterView.as_view(), name="register"),
    path(
        "logowanie/",
        auth_views.LoginView.as_view(
            template_name="registration/login.html",
            authentication_form=EmailAuthenticationForm,
        ),
        name="login",
    ),
    path("wyloguj/", auth_views.LogoutView.as_view(), name="logout"),
]
