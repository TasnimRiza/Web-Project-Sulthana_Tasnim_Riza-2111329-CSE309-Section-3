from django import forms

from .models import AcademicYear, ClassRoom, School, Section, Subject


class SchoolForm(forms.ModelForm):
    class Meta:
        model = School
        fields = "__all__"


class AcademicYearForm(forms.ModelForm):
    class Meta:
        model = AcademicYear
        fields = "__all__"


class ClassRoomForm(forms.ModelForm):
    class Meta:
        model = ClassRoom
        fields = "__all__"


class SectionForm(forms.ModelForm):
    class Meta:
        model = Section
        fields = "__all__"


class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = "__all__"
