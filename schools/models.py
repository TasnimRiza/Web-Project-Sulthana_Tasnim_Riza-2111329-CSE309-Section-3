from django.conf import settings
from django.db import models


class School(models.Model):
    name = models.CharField(max_length=180)
    code = models.CharField(max_length=40, unique=True)
    upazila = models.CharField(max_length=120)
    district = models.CharField(max_length=120)
    address = models.TextField(blank=True)
    phone = models.CharField(max_length=30, blank=True)
    head_teacher = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="headed_schools",
    )
    ueo = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="monitored_schools",
    )
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class AcademicYear(models.Model):
    name = models.CharField(max_length=20, unique=True)
    starts_on = models.DateField()
    ends_on = models.DateField()
    is_current = models.BooleanField(default=False)

    class Meta:
        ordering = ["-starts_on"]

    def __str__(self):
        return self.name


class ClassRoom(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name="classrooms")
    name = models.CharField(max_length=50)
    numeric_level = models.PositiveSmallIntegerField()
    class_teacher = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="class_teacher_rooms",
    )

    class Meta:
        ordering = ["school__name", "numeric_level", "name"]
        unique_together = ("school", "name")

    def __str__(self):
        return f"{self.school} - {self.name}"


class Section(models.Model):
    classroom = models.ForeignKey(ClassRoom, on_delete=models.CASCADE, related_name="sections")
    name = models.CharField(max_length=30)

    class Meta:
        ordering = ["classroom", "name"]
        unique_together = ("classroom", "name")

    def __str__(self):
        return f"{self.classroom} {self.name}"


class Subject(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name="subjects")
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=30)
    teachers = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name="subjects_taught")
    classrooms = models.ManyToManyField(ClassRoom, blank=True, related_name="subjects")

    class Meta:
        ordering = ["name"]
        unique_together = ("school", "code")

    def __str__(self):
        return self.name

# Create your models here.
