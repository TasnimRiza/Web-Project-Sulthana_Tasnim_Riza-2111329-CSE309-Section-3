from django.conf import settings
from django.db import models


class UserProfile(models.Model):
    TEACHER = "Teacher"
    STUDENT = "Student"
    GUARDIAN = "Guardian"
    HEAD_TEACHER = "HeadTeacher"
    UEO = "UEO"
    ADMIN = "Admin"

    ROLE_CHOICES = [
        (TEACHER, "Teacher"),
        (STUDENT, "Student"),
        (GUARDIAN, "Guardian"),
        (HEAD_TEACHER, "Head Teacher"),
        (UEO, "Upazila Education Officer"),
        (ADMIN, "Admin"),
    ]

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="smms_profile")
    role = models.CharField(max_length=30, choices=ROLE_CHOICES, default=STUDENT)
    school = models.ForeignKey("schools.School", on_delete=models.SET_NULL, null=True, blank=True, related_name="users")
    upazila = models.CharField(max_length=120, blank=True)
    phone = models.CharField(max_length=30, blank=True)
    address = models.TextField(blank=True)
    photo = models.ImageField(upload_to="profiles/", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["user__username"]

    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username} - {self.get_role_display()}"

    @property
    def is_school_leader(self):
        return self.role in {self.HEAD_TEACHER, self.ADMIN}

# Create your models here.
