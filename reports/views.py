import csv

from django.http import HttpResponse
from django.shortcuts import render

from accounts.decorators import role_required
from academics.models import Mark
from attendance.models import AttendanceRecord
from inspections.models import Inspection
from stipend.models import StipendApplication
from students.models import Student


@role_required("Teacher", "HeadTeacher", "UEO", "Admin")
def report_center(request):
    return render(request, "reports/center.html")


@role_required("Teacher", "HeadTeacher", "UEO", "Admin")
def attendance_csv(request):
    return _csv_response(
        "attendance_report.csv",
        ["Student", "Date", "Class", "Status"],
        ((r.student.name, r.attendance.date, r.attendance.classroom.name, r.status) for r in AttendanceRecord.objects.select_related("student", "attendance__classroom")),
    )


@role_required("Teacher", "HeadTeacher", "UEO", "Admin")
def marks_csv(request):
    return _csv_response(
        "marksheet.csv",
        ["Student", "Subject", "Exam", "Total", "Grade", "Rank", "Verified"],
        ((m.student.name, m.subject.name, m.exam.name, m.total, m.grade.letter if m.grade else "", m.rank or "", m.verification_status) for m in Mark.objects.select_related("student", "subject", "exam", "grade")),
    )


@role_required("HeadTeacher", "UEO", "Admin")
def stipend_csv(request):
    return _csv_response(
        "stipend_report.csv",
        ["Student", "Academic Year", "Attendance", "GPA", "Eligible", "Status"],
        (
            (
                a.student.name,
                a.academic_year.name,
                a.eligibility.attendance_percent if a.eligibility else "",
                a.eligibility.gpa if a.eligibility else "",
                a.eligibility.is_eligible if a.eligibility else "",
                a.status,
            )
            for a in StipendApplication.objects.select_related("student", "academic_year", "eligibility")
        ),
    )


@role_required("HeadTeacher", "UEO", "Admin")
def inspection_csv(request):
    return _csv_response(
        "inspection_report.csv",
        ["School", "Scheduled", "Focus", "Score", "Status"],
        ((i.school.name, i.scheduled_on, i.focus_area, i.score, i.status) for i in Inspection.objects.select_related("school")),
    )


@role_required("HeadTeacher", "UEO", "Admin")
def progress_csv(request):
    return _csv_response(
        "student_progress_report.csv",
        ["Student", "Attendance %", "GPA"],
        ((s.name, s.attendance_percentage(), s.average_gpa()) for s in Student.objects.all()),
    )


def _csv_response(filename, headers, rows):
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = f'attachment; filename="{filename}"'
    writer = csv.writer(response)
    writer.writerow(headers)
    writer.writerows(rows)
    return response

# Create your views here.
