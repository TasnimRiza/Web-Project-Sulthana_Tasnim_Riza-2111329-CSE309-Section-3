from django.conf import settings
from django.db import models


class Inspection(models.Model):
    SCHEDULED = "Scheduled"
    COMPLETED = "Completed"
    FOLLOW_UP = "Follow-up Required"
    STATUS_CHOICES = [(SCHEDULED, "Scheduled"), (COMPLETED, "Completed"), (FOLLOW_UP, "Follow-up Required")]

    school = models.ForeignKey("schools.School", on_delete=models.CASCADE, related_name="inspections")
    ueo = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="inspections")
    scheduled_on = models.DateField()
    visited_on = models.DateField(null=True, blank=True)
    focus_area = models.CharField(max_length=160)
    findings = models.TextField(blank=True)
    score = models.PositiveSmallIntegerField(default=0)
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default=SCHEDULED)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-scheduled_on"]

    def __str__(self):
        return f"{self.school} inspection"


class InspectionEvidence(models.Model):
    inspection = models.ForeignKey(Inspection, on_delete=models.CASCADE, related_name="evidence_items")
    title = models.CharField(max_length=140)
    file = models.FileField(upload_to="inspection_evidence/")
    note = models.TextField(blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Intervention(models.Model):
    OPEN = "Open"
    IN_PROGRESS = "In Progress"
    RESOLVED = "Resolved"
    STATUS_CHOICES = [(OPEN, "Open"), (IN_PROGRESS, "In Progress"), (RESOLVED, "Resolved")]

    inspection = models.ForeignKey(Inspection, on_delete=models.CASCADE, related_name="interventions")
    title = models.CharField(max_length=160)
    action_plan = models.TextField()
    assigned_to = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="interventions")
    due_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default=OPEN)

    class Meta:
        ordering = ["status", "due_date"]

    def __str__(self):
        return self.title

# Create your models here.
