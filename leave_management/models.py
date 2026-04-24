from django.conf import settings
from django.db import models


class LeaveRequest(models.Model):
    PENDING = "Pending"
    APPROVED = "Approved"
    REJECTED = "Rejected"
    STATUS_CHOICES = [(PENDING, "Pending"), (APPROVED, "Approved"), (REJECTED, "Rejected")]

    teacher = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="leave_requests")
    school = models.ForeignKey("schools.School", on_delete=models.CASCADE, related_name="leave_requests")
    leave_type = models.CharField(max_length=80)
    starts_on = models.DateField()
    ends_on = models.DateField()
    reason = models.TextField()
    attachment = models.FileField(upload_to="leave/", blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=PENDING)
    reviewed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="leave_reviews",
    )
    reviewed_at = models.DateTimeField(null=True, blank=True)
    review_note = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.teacher} leave ({self.status})"

# Create your models here.
