from django.shortcuts import render

from accounts.decorators import role_required

from .models import AuditLog


@role_required("Admin")
def audit_logs(request):
    logs = AuditLog.objects.select_related("user")[:200]
    return render(request, "audit/logs.html", {"logs": logs})

# Create your views here.
