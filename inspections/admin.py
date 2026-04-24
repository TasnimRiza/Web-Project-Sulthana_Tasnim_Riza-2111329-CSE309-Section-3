from django.contrib import admin

from .models import Inspection, InspectionEvidence, Intervention


admin.site.register(Inspection)
admin.site.register(InspectionEvidence)
admin.site.register(Intervention)

# Register your models here.
