from django.contrib import admin

from .models import StipendApplication, StipendEligibility


admin.site.register(StipendEligibility)
admin.site.register(StipendApplication)

# Register your models here.
