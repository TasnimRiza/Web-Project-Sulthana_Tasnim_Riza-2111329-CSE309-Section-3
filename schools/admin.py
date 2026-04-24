from django.contrib import admin

from .models import AcademicYear, ClassRoom, School, Section, Subject


admin.site.register(School)
admin.site.register(AcademicYear)
admin.site.register(ClassRoom)
admin.site.register(Section)
admin.site.register(Subject)

# Register your models here.
