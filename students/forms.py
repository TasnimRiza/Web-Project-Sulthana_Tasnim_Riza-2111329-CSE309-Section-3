from django import forms

from .models import Enrollment, Guardian, Student, StudentProfile


class GuardianForm(forms.ModelForm):
    class Meta:
        model = Guardian
        fields = "__all__"


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = "__all__"


class StudentProfileForm(forms.ModelForm):
    class Meta:
        model = StudentProfile
        fields = "__all__"


class EnrollmentForm(forms.ModelForm):
    class Meta:
        model = Enrollment
        fields = "__all__"
