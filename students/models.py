from django.conf import settings
from django.db import models


class Guardian(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="guardian_record")
    name = models.CharField(max_length=120)
    relationship = models.CharField(max_length=40, default="Parent")
    phone = models.CharField(max_length=30)
    email = models.EmailField(blank=True)
    address = models.TextField(blank=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Student(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="student_record")
    student_id = models.CharField(max_length=40, unique=True)
    name = models.CharField(max_length=120)
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=20, blank=True)
    school = models.ForeignKey("schools.School", on_delete=models.CASCADE, related_name="students")
    guardian = models.ForeignKey(Guardian, on_delete=models.SET_NULL, null=True, blank=True, related_name="students")
    admission_date = models.DateField(null=True, blank=True)
    photo = models.ImageField(upload_to="students/photos/", blank=True)
    birth_certificate = models.FileField(upload_to="students/documents/", blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} ({self.student_id})"

    def attendance_percentage(self):
        records = self.attendance_records.all()
        total = records.count()
        if total == 0:
            return 0
        present = records.filter(status__in=["Present", "Late"]).count()
        return round((present / total) * 100, 2)

    def average_gpa(self):
        marks = self.marks.all()
        if not marks:
            return 0
        return round(sum(mark.grade_point for mark in marks) / marks.count(), 2)


class StudentProfile(models.Model):
    student = models.OneToOneField(Student, on_delete=models.CASCADE, related_name="profile")
    blood_group = models.CharField(max_length=10, blank=True)
    health_notes = models.TextField(blank=True)
    learning_needs = models.TextField(blank=True)
    emergency_contact = models.CharField(max_length=30, blank=True)

    def __str__(self):
        return f"Profile for {self.student}"


class Enrollment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="enrollments")
    academic_year = models.ForeignKey("schools.AcademicYear", on_delete=models.PROTECT, related_name="enrollments")
    classroom = models.ForeignKey("schools.ClassRoom", on_delete=models.PROTECT, related_name="enrollments")
    section = models.ForeignKey("schools.Section", on_delete=models.SET_NULL, null=True, blank=True, related_name="enrollments")
    roll_number = models.PositiveIntegerField()
    is_current = models.BooleanField(default=True)

    class Meta:
        ordering = ["classroom", "roll_number"]
        unique_together = ("academic_year", "classroom", "section", "roll_number")

    def __str__(self):
        return f"{self.student} - {self.classroom}"

# Create your models here.
