from django.conf import settings
from django.db import models


class Exam(models.Model):
    name = models.CharField(max_length=100)
    academic_year = models.ForeignKey("schools.AcademicYear", on_delete=models.CASCADE, related_name="exams")
    starts_on = models.DateField(null=True, blank=True)
    ends_on = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ["-starts_on", "name"]

    def __str__(self):
        return f"{self.name} - {self.academic_year}"


class Grade(models.Model):
    letter = models.CharField(max_length=5, unique=True)
    min_score = models.PositiveSmallIntegerField()
    max_score = models.PositiveSmallIntegerField()
    point = models.DecimalField(max_digits=3, decimal_places=2)

    class Meta:
        ordering = ["-point"]

    def __str__(self):
        return f"{self.letter} ({self.point})"


class Mark(models.Model):
    PENDING = "Pending"
    VERIFIED = "Verified"
    REJECTED = "Rejected"
    STATUS_CHOICES = [(PENDING, "Pending"), (VERIFIED, "Verified"), (REJECTED, "Rejected")]

    student = models.ForeignKey("students.Student", on_delete=models.CASCADE, related_name="marks")
    subject = models.ForeignKey("schools.Subject", on_delete=models.CASCADE, related_name="marks")
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name="marks")
    written = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    oral = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    practical = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    grade = models.ForeignKey(Grade, on_delete=models.SET_NULL, null=True, blank=True, related_name="marks")
    rank = models.PositiveIntegerField(null=True, blank=True)
    submitted_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="marks_submitted")
    verification_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=PENDING)
    verified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="marks_verified",
    )
    verified_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["exam", "subject", "-total"]
        unique_together = ("student", "subject", "exam")

    def save(self, *args, **kwargs):
        self.total = self.written + self.oral + self.practical
        self.grade = Grade.objects.filter(min_score__lte=self.total, max_score__gte=self.total).first()
        super().save(*args, **kwargs)

    @property
    def grade_point(self):
        return float(self.grade.point) if self.grade else 0

    def __str__(self):
        return f"{self.student} - {self.subject} - {self.total}"


class SyllabusProgress(models.Model):
    subject = models.ForeignKey("schools.Subject", on_delete=models.CASCADE, related_name="syllabus_progress")
    classroom = models.ForeignKey("schools.ClassRoom", on_delete=models.CASCADE, related_name="syllabus_progress")
    chapter = models.CharField(max_length=150)
    target_date = models.DateField()
    completed_date = models.DateField(null=True, blank=True)
    progress_percent = models.PositiveSmallIntegerField(default=0)
    submitted_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="syllabus_updates")
    is_verified = models.BooleanField(default=False)

    class Meta:
        ordering = ["target_date"]

    @property
    def is_delayed(self):
        from django.utils import timezone

        return self.progress_percent < 100 and self.target_date < timezone.localdate()

    def __str__(self):
        return f"{self.subject} - {self.chapter}"


class ClassActivity(models.Model):
    classroom = models.ForeignKey("schools.ClassRoom", on_delete=models.CASCADE, related_name="activities")
    subject = models.ForeignKey("schools.Subject", on_delete=models.CASCADE, related_name="activities")
    date = models.DateField()
    topic = models.CharField(max_length=160)
    activity_type = models.CharField(max_length=80, blank=True)
    summary = models.TextField()
    evidence = models.FileField(upload_to="class_activities/", blank=True)
    submitted_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="class_activities")
    is_verified = models.BooleanField(default=False)

    class Meta:
        ordering = ["-date"]

    def __str__(self):
        return f"{self.classroom} - {self.topic}"

# Create your models here.
