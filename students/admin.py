from django.contrib import admin

from .models import Enrollment, Guardian, Student, StudentProfile


admin.site.register(Guardian)
admin.site.register(Student)
admin.site.register(StudentProfile)
admin.site.register(Enrollment)

# Register your models here.
