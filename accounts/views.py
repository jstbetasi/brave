from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView

from .forms import RegisterForm


class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = "accounts/register.html"
    success_url = reverse_lazy("panel")

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        return response


class PanelView(LoginRequiredMixin, TemplateView):
    template_name = "accounts/panel.html"
