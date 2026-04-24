from django import forms

from .models import ClassActivity, Exam, Grade, Mark, SyllabusProgress


class ExamForm(forms.ModelForm):
    class Meta:
        model = Exam
        fields = "__all__"
        widgets = {"starts_on": forms.DateInput(attrs={"type": "date"}), "ends_on": forms.DateInput(attrs={"type": "date"})}


class GradeForm(forms.ModelForm):
    class Meta:
        model = Grade
        fields = "__all__"


class MarkForm(forms.ModelForm):
    class Meta:
        model = Mark
        fields = ("student", "subject", "exam", "written", "oral", "practical")


class SyllabusProgressForm(forms.ModelForm):
    class Meta:
        model = SyllabusProgress
        fields = ("subject", "classroom", "chapter", "target_date", "completed_date", "progress_percent")
        widgets = {"target_date": forms.DateInput(attrs={"type": "date"}), "completed_date": forms.DateInput(attrs={"type": "date"})}


class ClassActivityForm(forms.ModelForm):
    class Meta:
        model = ClassActivity
        fields = ("classroom", "subject", "date", "topic", "activity_type", "summary", "evidence")
        widgets = {"date": forms.DateInput(attrs={"type": "date"})}
