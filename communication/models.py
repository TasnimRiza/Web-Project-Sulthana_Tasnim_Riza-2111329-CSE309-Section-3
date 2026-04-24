from django.conf import settings
from django.db import models


class Notice(models.Model):
    TARGET_CHOICES = [
        ("All", "All"),
        ("Teacher", "Teachers"),
        ("Student", "Students"),
        ("Guardian", "Guardians"),
        ("HeadTeacher", "Head Teachers"),
        ("UEO", "UEOs"),
    ]

    title = models.CharField(max_length=180)
    body = models.TextField()
    school = models.ForeignKey("schools.School", on_delete=models.CASCADE, null=True, blank=True, related_name="notices")
    target_role = models.CharField(max_length=30, choices=TARGET_CHOICES, default="All")
    published_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="published_notices")
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title


class Message(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="sent_messages")
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="received_messages")
    subject = models.CharField(max_length=160)
    body = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.subject

# Create your models here.
