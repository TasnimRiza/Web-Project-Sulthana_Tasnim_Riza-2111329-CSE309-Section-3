from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from accounts.decorators import role_required
from audit.models import log_action

from .forms import ClassActivityForm, ExamForm, GradeForm, MarkForm, SyllabusProgressForm
from .models import ClassActivity, Exam, Grade, Mark, SyllabusProgress


@role_required("Teacher", "HeadTeacher", "Admin", "UEO")
def academic_home(request):
    context = {
        "marks": Mark.objects.select_related("student", "subject", "exam")[:20],
        "syllabus": SyllabusProgress.objects.select_related("subject", "classroom")[:20],
        "activities": ClassActivity.objects.select_related("classroom", "subject")[:20],
    }
    return render(request, "academics/home.html", context)


@role_required("Teacher")
def mark_create(request):
    form = MarkForm(request.POST or None)
    if form.is_valid():
        mark = form.save(commit=False)
        mark.submitted_by = request.user
        mark.save()
        update_rankings(mark.exam, mark.subject)
        log_action(request.user, "submitted mark", mark, request=request)
        return redirect("academics:home")
    return render(request, "smms/form.html", {"form": form, "title": "Enter Marks"})


def update_rankings(exam, subject):
    marks = Mark.objects.filter(exam=exam, subject=subject).order_by("-total")
    for index, mark in enumerate(marks, start=1):
        if mark.rank != index:
            mark.rank = index
            mark.save(update_fields=["rank"])


@role_required("Teacher")
def syllabus_create(request):
    form = SyllabusProgressForm(request.POST or None)
    if form.is_valid():
        progress = form.save(commit=False)
        progress.submitted_by = request.user
        progress.save()
        log_action(request.user, "submitted syllabus progress", progress, request=request)
        return redirect("academics:home")
    return render(request, "smms/form.html", {"form": form, "title": "Update Syllabus Progress"})


@role_required("Teacher")
def activity_create(request):
    form = ClassActivityForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        activity = form.save(commit=False)
        activity.submitted_by = request.user
        activity.save()
        log_action(request.user, "submitted class activity", activity, request=request)
        return redirect("academics:home")
    return render(request, "smms/form.html", {"form": form, "title": "Record Class Activity"})


@role_required("HeadTeacher", "Admin")
def verify_mark(request, pk, status):
    mark = get_object_or_404(Mark, pk=pk)
    mark.verification_status = Mark.VERIFIED if status == "approve" else Mark.REJECTED
    mark.verified_by = request.user
    mark.verified_at = timezone.now()
    mark.save()
    log_action(request.user, f"{mark.verification_status.lower()} mark", mark, request=request)
    return redirect("academics:home")


@role_required("Admin", "HeadTeacher")
def exam_create(request):
    form = ExamForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect("academics:home")
    return render(request, "smms/form.html", {"form": form, "title": "Add Exam"})


@role_required("Admin")
def grade_create(request):
    form = GradeForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect("academics:home")
    return render(request, "smms/form.html", {"form": form, "title": "Add Grade"})

# Create your views here.
