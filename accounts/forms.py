from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User


class RegisterForm(UserCreationForm):
    email = forms.EmailField(label="Email", required=True)

    field_order = ["email", "password1", "password2"]

    class Meta:
        model = User
        fields = ("email",)

    def clean_email(self):
        email = self.cleaned_data["email"]
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("Konto z tym adresem email już istnieje.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data["email"]
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user


class EmailAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(label="Email")
