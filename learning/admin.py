from django.contrib import admin

from .models import AdultProfile, ChildProfile, ExerciseAttempt, LessonAssignment, Letter, LetterProgress


@admin.register(AdultProfile)
class AdultProfileAdmin(admin.ModelAdmin):
    list_display = ("display_name", "role", "user", "organization", "created_at")
    list_filter = ("role",)
    search_fields = ("display_name", "user__username", "organization")


@admin.register(Letter)
class LetterAdmin(admin.ModelAdmin):
    list_display = ("symbol", "language", "word", "sort_order", "is_active")
    list_filter = ("language", "is_active")
    search_fields = ("symbol", "word", "description")


@admin.register(ChildProfile)
class ChildProfileAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "preferred_language",
        "owner",
        "stars",
        "inclusive_mode",
        "audio_first_mode",
        "created_at",
    )
    list_filter = ("preferred_language", "inclusive_mode", "audio_first_mode")
    search_fields = ("name", "owner__username")


@admin.register(LetterProgress)
class LetterProgressAdmin(admin.ModelAdmin):
    list_display = (
        "profile",
        "letter",
        "views_count",
        "correct_answers",
        "incorrect_answers",
        "completed",
        "last_viewed_at",
    )
    list_filter = ("completed", "letter__language")


@admin.register(ExerciseAttempt)
class ExerciseAttemptAdmin(admin.ModelAdmin):
    list_display = ("profile", "language", "exercise_type", "score", "total_questions", "created_at")
    list_filter = ("language", "exercise_type", "created_at")


@admin.register(LessonAssignment)
class LessonAssignmentAdmin(admin.ModelAdmin):
    list_display = ("title", "teacher", "child", "language", "due_date", "is_active")
    list_filter = ("language", "is_active")
    search_fields = ("title", "child__name", "teacher__display_name")
    filter_horizontal = ("letters",)
