from django.db.models import Q
from django.shortcuts import redirect, render

from accounts.decorators import role_required
from audit.models import log_action

from .forms import EnrollmentForm, GuardianForm, StudentForm, StudentProfileForm
from .models import Enrollment, Guardian, Student, StudentProfile


@role_required("Admin", "HeadTeacher", "Teacher", "UEO")
def student_list(request):
    query = request.GET.get("q", "")
    students = Student.objects.select_related("school", "guardian")
    if query:
        students = students.filter(Q(name__icontains=query) | Q(student_id__icontains=query) | Q(school__name__icontains=query))
    return render(request, "students/list.html", {"students": students, "query": query})


@role_required("Admin", "HeadTeacher")
def student_create(request):
    if request.method == "POST":
        form = StudentForm(request.POST, request.FILES)
        if form.is_valid():
            student = form.save()
            StudentProfile.objects.get_or_create(student=student)
            log_action(request.user, "created", student, request=request)
            return redirect("students:list")
    else:
        form = StudentForm()
    return render(request, "smms/form.html", {"form": form, "title": "Register Student"})


@role_required("Admin", "HeadTeacher")
def guardian_create(request):
    form = GuardianForm(request.POST or None)
    if form.is_valid():
        guardian = form.save()
        log_action(request.user, "created", guardian, request=request)
        return redirect("students:list")
    return render(request, "smms/form.html", {"form": form, "title": "Add Guardian"})


@role_required("Admin", "HeadTeacher")
def enrollment_create(request):
    form = EnrollmentForm(request.POST or None)
    if form.is_valid():
        enrollment = form.save()
        log_action(request.user, "created", enrollment, request=request)
        return redirect("students:list")
    return render(request, "smms/form.html", {"form": form, "title": "Enroll Student"})


@role_required("Admin", "HeadTeacher", "Teacher", "Student", "Guardian", "UEO")
def student_detail(request, pk):
    student = Student.objects.select_related("school", "guardian").get(pk=pk)
    role = getattr(request.user.smms_profile, "role", None)
    if role == "Student" and student.user_id != request.user.id:
        from django.core.exceptions import PermissionDenied

        raise PermissionDenied
    if role == "Guardian" and (not student.guardian or student.guardian.user_id != request.user.id):
        from django.core.exceptions import PermissionDenied

        raise PermissionDenied
    return render(request, "students/detail.html", {"student": student})

# Create your views here.
