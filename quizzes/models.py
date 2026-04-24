from django.conf import settings
from django.db import models


class Quiz(models.Model):
    student = models.ForeignKey("students.Student", on_delete=models.CASCADE, related_name="quizzes")
    subject = models.ForeignKey("schools.Subject", on_delete=models.CASCADE, related_name="quizzes")
    chapter = models.CharField(max_length=150)
    generated_by_ai = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.subject} quiz for {self.student}"


class QuizQuestion(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="questions")
    question = models.TextField()
    option_a = models.CharField(max_length=255)
    option_b = models.CharField(max_length=255)
    option_c = models.CharField(max_length=255, blank=True)
    option_d = models.CharField(max_length=255, blank=True)
    correct_option = models.CharField(max_length=1, default="A")
    explanation = models.TextField(blank=True)

    def __str__(self):
        return self.question[:80]


class QuizAttempt(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="attempts")
    student_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="quiz_attempts")
    answers = models.JSONField(default=dict, blank=True)
    score = models.PositiveSmallIntegerField(default=0)
    total = models.PositiveSmallIntegerField(default=0)
    feedback = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.quiz} attempt {self.score}/{self.total}"


class Reward(models.Model):
    student = models.ForeignKey("students.Student", on_delete=models.CASCADE, related_name="rewards")
    title = models.CharField(max_length=120)
    badge = models.CharField(max_length=80, default="Star")
    points = models.PositiveIntegerField(default=0)
    earned_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-earned_at"]

    def __str__(self):
        return f"{self.student} - {self.title}"

# Create your models here.
