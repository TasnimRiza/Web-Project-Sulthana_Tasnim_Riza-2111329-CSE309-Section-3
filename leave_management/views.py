from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from accounts.decorators import role_required
from audit.models import log_action

from .forms import LeaveRequestForm
from .models import LeaveRequest


@role_required("Teacher", "HeadTeacher", "Admin")
def leave_list(request):
    leaves = LeaveRequest.objects.select_related("teacher", "school", "reviewed_by")
    if request.user.smms_profile.role == "Teacher":
        leaves = leaves.filter(teacher=request.user)
    return render(request, "leave_management/list.html", {"leaves": leaves})


@role_required("Teacher")
def leave_create(request):
    form = LeaveRequestForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        leave = form.save(commit=False)
        leave.teacher = request.user
        leave.save()
        log_action(request.user, "submitted leave request", leave, request=request)
        return redirect("leave_management:list")
    return render(request, "smms/form.html", {"form": form, "title": "Submit Leave Request"})


@role_required("HeadTeacher", "Admin")
def review_leave(request, pk, status):
    leave = get_object_or_404(LeaveRequest, pk=pk)
    leave.status = LeaveRequest.APPROVED if status == "approve" else LeaveRequest.REJECTED
    leave.reviewed_by = request.user
    leave.reviewed_at = timezone.now()
    leave.save()
    log_action(request.user, f"{leave.status.lower()} leave request", leave, request=request)
    return redirect("leave_management:list")

# Create your views here.
