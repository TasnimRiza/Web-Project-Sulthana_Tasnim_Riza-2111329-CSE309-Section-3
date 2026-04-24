from django import forms

from .models import Attendance, AttendanceRecord


class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ("classroom", "section", "date", "note")
        widgets = {"date": forms.DateInput(attrs={"type": "date"})}


class AttendanceRecordForm(forms.ModelForm):
    class Meta:
        model = AttendanceRecord
        fields = ("student", "status", "remark")
