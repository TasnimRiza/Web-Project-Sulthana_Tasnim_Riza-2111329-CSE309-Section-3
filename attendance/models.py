from django.conf import settings
from django.db import models


class Attendance(models.Model):
    PENDING = "Pending"
    VERIFIED = "Verified"
    REJECTED = "Rejected"
    STATUS_CHOICES = [(PENDING, "Pending"), (VERIFIED, "Verified"), (REJECTED, "Rejected")]

    classroom = models.ForeignKey("schools.ClassRoom", on_delete=models.CASCADE, related_name="attendance_sheets")
    section = models.ForeignKey("schools.Section", on_delete=models.SET_NULL, null=True, blank=True, related_name="attendance_sheets")
    date = models.DateField()
    taken_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="attendance_taken")
    verification_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=PENDING)
    verified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="attendance_verified",
    )
    verified_at = models.DateTimeField(null=True, blank=True)
    note = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-date", "classroom"]
        unique_together = ("classroom", "section", "date")

    def __str__(self):
        return f"{self.classroom} attendance on {self.date}"

    @property
    def present_percentage(self):
        total = self.records.count()
        if total == 0:
            return 0
        present = self.records.filter(status__in=[AttendanceRecord.PRESENT, AttendanceRecord.LATE]).count()
        return round((present / total) * 100, 2)

    @property
    def has_low_attendance_alert(self):
        return self.present_percentage < 75


class AttendanceRecord(models.Model):
    PRESENT = "Present"
    ABSENT = "Absent"
    LATE = "Late"
    EXCUSED = "Excused"
    STATUS_CHOICES = [(PRESENT, "Present"), (ABSENT, "Absent"), (LATE, "Late"), (EXCUSED, "Excused")]

    attendance = models.ForeignKey(Attendance, on_delete=models.CASCADE, related_name="records")
    student = models.ForeignKey("students.Student", on_delete=models.CASCADE, related_name="attendance_records")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=PRESENT)
    remark = models.CharField(max_length=255, blank=True)

    class Meta:
        ordering = ["student__name"]
        unique_together = ("attendance", "student")

    def __str__(self):
        return f"{self.student} - {self.status}"

# Create your models here.
