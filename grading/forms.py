from django import forms


class EssayForm(forms.Form):
    autor = forms.CharField(
        label="Autor",
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={"placeholder": "np. Jan Kowalski"}),
    )
    tekst = forms.CharField(
        label="Tekst eseju",
        widget=forms.Textarea(attrs={"rows": 20}),
    )

    def clean_tekst(self):
        tekst = self.cleaned_data["tekst"].strip()
        if not tekst:
            raise forms.ValidationError("Wklej treść eseju przed oddaniem do oceny.")
        return tekst
