from django import forms

from .models import StipendApplication


class StipendApplicationForm(forms.ModelForm):
    class Meta:
        model = StipendApplication
        fields = ("student", "academic_year", "amount", "bank_account")
