from django.contrib import admin

from .models import ClassActivity, Exam, Grade, Mark, SyllabusProgress


admin.site.register(Exam)
admin.site.register(Grade)
admin.site.register(Mark)
admin.site.register(SyllabusProgress)
admin.site.register(ClassActivity)

# Register your models here.
