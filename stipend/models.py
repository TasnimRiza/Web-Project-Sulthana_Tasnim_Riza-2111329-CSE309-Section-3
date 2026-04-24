from django.conf import settings
from django.db import models


class StipendEligibility(models.Model):
    student = models.OneToOneField("students.Student", on_delete=models.CASCADE, related_name="stipend_eligibility")
    attendance_percent = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    gpa = models.DecimalField(max_digits=4, decimal_places=2, default=0)
    is_eligible = models.BooleanField(default=False)
    calculated_at = models.DateTimeField(auto_now=True)
    validated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="stipend_validations",
    )
    is_validated = models.BooleanField(default=False)

    def recalculate(self):
        self.attendance_percent = self.student.attendance_percentage()
        self.gpa = self.student.average_gpa()
        self.is_eligible = self.attendance_percent >= 85 and self.gpa >= 3.80
        self.save()
        return self

    def __str__(self):
        return f"{self.student} stipend eligibility"


class StipendApplication(models.Model):
    PENDING = "Pending"
    VALIDATED = "Validated"
    REJECTED = "Rejected"
    PAID = "Paid"
    STATUS_CHOICES = [(PENDING, "Pending"), (VALIDATED, "Validated"), (REJECTED, "Rejected"), (PAID, "Paid")]

    student = models.ForeignKey("students.Student", on_delete=models.CASCADE, related_name="stipend_applications")
    academic_year = models.ForeignKey("schools.AcademicYear", on_delete=models.PROTECT, related_name="stipend_applications")
    eligibility = models.ForeignKey(StipendEligibility, on_delete=models.SET_NULL, null=True, blank=True, related_name="applications")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=PENDING)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    bank_account = models.CharField(max_length=80, blank=True)
    reviewed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="stipend_reviews")
    review_note = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        unique_together = ("student", "academic_year")

    def __str__(self):
        return f"{self.student} - {self.status}"

# Create your models here.
