from django import forms

from .models import Inspection, InspectionEvidence, Intervention


class InspectionForm(forms.ModelForm):
    class Meta:
        model = Inspection
        fields = ("school", "scheduled_on", "visited_on", "focus_area", "findings", "score", "status")
        widgets = {"scheduled_on": forms.DateInput(attrs={"type": "date"}), "visited_on": forms.DateInput(attrs={"type": "date"})}


class InspectionEvidenceForm(forms.ModelForm):
    class Meta:
        model = InspectionEvidence
        fields = "__all__"


class InterventionForm(forms.ModelForm):
    class Meta:
        model = Intervention
        fields = "__all__"
        widgets = {"due_date": forms.DateInput(attrs={"type": "date"})}
