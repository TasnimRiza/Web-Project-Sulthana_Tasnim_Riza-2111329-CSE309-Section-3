from django.shortcuts import get_object_or_404, redirect, render

from accounts.decorators import role_required
from audit.models import log_action

from .forms import StipendApplicationForm
from .models import StipendApplication, StipendEligibility


@role_required("Student", "Guardian", "HeadTeacher", "Admin", "UEO")
def stipend_list(request):
    applications = StipendApplication.objects.select_related("student", "academic_year", "eligibility")
    return render(request, "stipend/list.html", {"applications": applications})


@role_required("HeadTeacher", "Admin")
def stipend_create(request):
    form = StipendApplicationForm(request.POST or None)
    if form.is_valid():
        app = form.save(commit=False)
        eligibility, _ = StipendEligibility.objects.get_or_create(student=app.student)
        eligibility.recalculate()
        app.eligibility = eligibility
        app.save()
        log_action(request.user, "created stipend application", app, request=request)
        return redirect("stipend:list")
    return render(request, "smms/form.html", {"form": form, "title": "Create Stipend Application"})


@role_required("HeadTeacher", "Admin")
def validate_stipend(request, pk):
    app = get_object_or_404(StipendApplication, pk=pk)
    eligibility, _ = StipendEligibility.objects.get_or_create(student=app.student)
    eligibility.recalculate()
    eligibility.validated_by = request.user
    eligibility.is_validated = True
    eligibility.save()
    app.eligibility = eligibility
    app.status = StipendApplication.VALIDATED if eligibility.is_eligible else StipendApplication.REJECTED
    app.reviewed_by = request.user
    app.save()
    log_action(request.user, "validated stipend eligibility", app, request=request)
    return redirect("stipend:list")

# Create your views here.
