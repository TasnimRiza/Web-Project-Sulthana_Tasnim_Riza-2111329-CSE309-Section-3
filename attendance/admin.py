from django.contrib import admin

from .models import Attendance, AttendanceRecord


class AttendanceRecordInline(admin.TabularInline):
    model = AttendanceRecord
    extra = 0


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ("classroom", "section", "date", "taken_by", "verification_status", "present_percentage")
    list_filter = ("verification_status", "date", "classroom__school")
    inlines = [AttendanceRecordInline]

# Register your models here.
