from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from accounts.decorators import role_required
from audit.models import log_action
from students.models import Enrollment

from .forms import AttendanceForm
from .models import Attendance, AttendanceRecord


@role_required("Teacher", "HeadTeacher", "Admin", "UEO")
def attendance_list(request):
    sheets = Attendance.objects.select_related("classroom", "section", "taken_by").prefetch_related("records")
    return render(request, "attendance/list.html", {"sheets": sheets})


@role_required("Teacher")
def take_attendance(request):
    if request.method == "POST":
        form = AttendanceForm(request.POST)
        if form.is_valid():
            attendance = form.save(commit=False)
            attendance.taken_by = request.user
            attendance.save()
            students = Enrollment.objects.filter(classroom=attendance.classroom, section=attendance.section, is_current=True).select_related("student")
            for enrollment in students:
                status = request.POST.get(f"student_{enrollment.student_id}", AttendanceRecord.PRESENT)
                AttendanceRecord.objects.create(attendance=attendance, student=enrollment.student, status=status)
            log_action(request.user, "submitted attendance", attendance, request=request)
            return redirect("attendance:list")
    else:
        form = AttendanceForm()
    return render(request, "attendance/take.html", {"form": form})


@role_required("HeadTeacher", "Admin")
def verify_attendance(request, pk, status):
    attendance = get_object_or_404(Attendance, pk=pk)
    attendance.verification_status = Attendance.VERIFIED if status == "approve" else Attendance.REJECTED
    attendance.verified_by = request.user
    attendance.verified_at = timezone.now()
    attendance.save()
    log_action(request.user, f"{attendance.verification_status.lower()} attendance", attendance, request=request)
    return redirect("attendance:list")

# Create your views here.
