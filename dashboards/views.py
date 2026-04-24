from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from academics.models import Mark, SyllabusProgress
from attendance.models import Attendance
from communication.models import Notice
from inspections.models import Inspection
from leave_management.models import LeaveRequest
from schools.models import School
from stipend.models import StipendApplication
from students.models import Student


@login_required
def home(request):
    role = request.user.smms_profile.role
    template = {
        "Teacher": "dashboards/teacher.html",
        "Student": "dashboards/student.html",
        "Guardian": "dashboards/student.html",
        "HeadTeacher": "dashboards/head_teacher.html",
        "UEO": "dashboards/ueo.html",
        "Admin": "dashboards/admin.html",
    }.get(role, "dashboards/admin.html")
    return render(request, template, dashboard_context(request, role))


def landing(request):
    if request.user.is_authenticated:
        return redirect("dashboards:home")
    return render(request, "dashboards/landing.html")


def dashboard_context(request, role):
    base = {
        "role": role,
        "notices": Notice.objects.filter(is_published=True)[:5],
        "students_count": Student.objects.count(),
        "schools_count": School.objects.count(),
        "low_attendance_count": sum(1 for item in Attendance.objects.all() if item.has_low_attendance_alert),
        "pending_attendance": Attendance.objects.filter(verification_status="Pending").count(),
        "pending_marks": Mark.objects.filter(verification_status="Pending").count(),
        "delayed_syllabus": [item for item in SyllabusProgress.objects.all() if item.is_delayed],
        "leave_requests": LeaveRequest.objects.filter(status="Pending")[:5],
        "stipends": StipendApplication.objects.select_related("student")[:5],
        "inspections": Inspection.objects.select_related("school")[:5],
    }
    if role == "Student" and hasattr(request.user, "student_record"):
        base["student"] = request.user.student_record
    if role == "Guardian" and hasattr(request.user, "guardian_record"):
        base["guardian_students"] = request.user.guardian_record.students.all()
    return base

# Create your views here.
