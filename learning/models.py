from django.conf import settings
from django.contrib.auth.models import User
from django.db import models


class AdultProfile(models.Model):
    ROLE_CHOICES = [
        ("parent", "Parent"),
        ("teacher", "Teacher"),
    ]

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="adult_profile")
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    display_name = models.CharField(max_length=100)
    organization = models.CharField(max_length=120, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.display_name} ({self.get_role_display()})"


class ChildProfile(models.Model):
    name = models.CharField(max_length=80, default="Little Learner")
    age_group = models.CharField(max_length=20, blank=True)
    preferred_language = models.CharField(max_length=20, default="english")
    stars = models.PositiveIntegerField(default=0)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="owned_children",
    )
    inclusive_mode = models.BooleanField(default=False)
    audio_first_mode = models.BooleanField(default=False)
    high_contrast_mode = models.BooleanField(default=False)
    large_text_mode = models.BooleanField(default=False)
    simplified_layout = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Letter(models.Model):
    LANGUAGE_CHOICES = [
        ("english", "English"),
        ("bangla", "Bangla"),
    ]

    language = models.CharField(max_length=20, choices=LANGUAGE_CHOICES)
    symbol = models.CharField(max_length=10)
    slug = models.SlugField(max_length=120, unique=True, blank=True)
    name = models.CharField(max_length=50)
    transliteration = models.CharField(max_length=50, blank=True)
    word = models.CharField(max_length=100)
    word_translation = models.CharField(max_length=120, blank=True)
    emoji = models.CharField(max_length=10, blank=True)
    description = models.CharField(max_length=255)
    speech_text = models.CharField(max_length=120)
    sort_order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["sort_order", "symbol"]
        unique_together = ("language", "symbol")

    def __str__(self):
        return f"{self.get_language_display()} - {self.symbol}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = f"{self.language}-{self.sort_order}"
        super().save(*args, **kwargs)


class LetterProgress(models.Model):
    profile = models.ForeignKey(
        ChildProfile,
        on_delete=models.CASCADE,
        related_name="letter_progress",
    )
    letter = models.ForeignKey(
        Letter,
        on_delete=models.CASCADE,
        related_name="progress_items",
    )
    views_count = models.PositiveIntegerField(default=0)
    correct_answers = models.PositiveIntegerField(default=0)
    incorrect_answers = models.PositiveIntegerField(default=0)
    completed = models.BooleanField(default=False)
    last_viewed_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("profile", "letter")

    def __str__(self):
        return f"{self.profile} -> {self.letter}"

    @property
    def strength_score(self):
        return self.correct_answers - self.incorrect_answers


class ExerciseAttempt(models.Model):
    profile = models.ForeignKey(
        ChildProfile,
        on_delete=models.CASCADE,
        related_name="attempts",
    )
    language = models.CharField(max_length=20)
    exercise_type = models.CharField(max_length=30, default="standard")
    score = models.PositiveIntegerField(default=0)
    total_questions = models.PositiveIntegerField(default=5)
    answers = models.JSONField(default=list, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.profile} - {self.language} ({self.score}/{self.total_questions})"


class LessonAssignment(models.Model):
    teacher = models.ForeignKey(AdultProfile, on_delete=models.CASCADE, related_name="assignments")
    child = models.ForeignKey(ChildProfile, on_delete=models.CASCADE, related_name="assignments")
    language = models.CharField(max_length=20, choices=Letter.LANGUAGE_CHOICES)
    title = models.CharField(max_length=120)
    note = models.TextField(blank=True)
    due_date = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    letters = models.ManyToManyField(Letter, related_name="lesson_assignments", blank=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.title} for {self.child.name}"
