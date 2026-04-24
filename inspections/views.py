from django.shortcuts import redirect, render

from accounts.decorators import role_required
from audit.models import log_action

from .forms import InspectionForm, InterventionForm
from .models import Inspection, Intervention


@role_required("UEO", "Admin", "HeadTeacher")
def inspection_list(request):
    inspections = Inspection.objects.select_related("school", "ueo")
    return render(request, "inspections/list.html", {"inspections": inspections})


@role_required("UEO", "Admin")
def inspection_create(request):
    form = InspectionForm(request.POST or None)
    if form.is_valid():
        inspection = form.save(commit=False)
        inspection.ueo = request.user
        inspection.save()
        log_action(request.user, "scheduled inspection", inspection, request=request)
        return redirect("inspections:list")
    return render(request, "smms/form.html", {"form": form, "title": "Schedule Inspection"})


@role_required("UEO", "Admin")
def intervention_create(request):
    form = InterventionForm(request.POST or None)
    if form.is_valid():
        intervention = form.save()
        log_action(request.user, "created intervention", intervention, request=request)
        return redirect("inspections:list")
    return render(request, "smms/form.html", {"form": form, "title": "Create Intervention"})

# Create your views here.
