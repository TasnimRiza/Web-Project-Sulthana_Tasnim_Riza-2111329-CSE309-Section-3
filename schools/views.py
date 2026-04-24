from django.shortcuts import redirect, render

from accounts.decorators import role_required
from audit.models import log_action

from .forms import AcademicYearForm, ClassRoomForm, SchoolForm, SectionForm, SubjectForm
from .models import AcademicYear, ClassRoom, School, Section, Subject


def _list(request, model, title, create_url=None):
    return render(request, "smms/list.html", {"title": title, "objects": model.objects.all(), "create_url": create_url})


def _create(request, form_class, title):
    if request.method == "POST":
        form = form_class(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save()
            log_action(request.user, "created", obj, request=request)
            return redirect("schools:schools")
    else:
        form = form_class()
    return render(request, "smms/form.html", {"title": title, "form": form})


@role_required("Admin", "HeadTeacher", "UEO")
def schools(request):
    return _list(request, School, "Schools", "schools:school-create")


@role_required("Admin", "HeadTeacher")
def school_create(request):
    return _create(request, SchoolForm, "Add School")


@role_required("Admin", "HeadTeacher")
def academic_year_create(request):
    return _create(request, AcademicYearForm, "Add Academic Year")


@role_required("Admin", "HeadTeacher")
def classroom_create(request):
    return _create(request, ClassRoomForm, "Add Class")


@role_required("Admin", "HeadTeacher")
def section_create(request):
    return _create(request, SectionForm, "Add Section")


@role_required("Admin", "HeadTeacher")
def subject_create(request):
    return _create(request, SubjectForm, "Add Subject")


@role_required("Admin", "HeadTeacher", "Teacher")
def setup(request):
    context = {
        "title": "Academic Setup",
        "schools": School.objects.count(),
        "classrooms": ClassRoom.objects.count(),
        "sections": Section.objects.count(),
        "subjects": Subject.objects.count(),
        "years": AcademicYear.objects.all(),
    }
    return render(request, "schools/setup.html", context)

# Create your views here.
