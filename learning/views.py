import random


from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Avg, Count, F, Q
from django.http import Http404, HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render

from .catalog import LANGUAGE_META
from .forms import AccessibilitySettingsForm, AdultLoginForm, AdultSignUpForm, LessonAssignmentForm
from .models import AdultProfile, ChildProfile, ExerciseAttempt, LessonAssignment, Letter, LetterProgress

EXERCISE_SIZE = 5


def get_adult_profile(request):
    if request.user.is_authenticated:
        return AdultProfile.objects.filter(user=request.user).first()
    return None


def get_current_profile(request):
    profile_id = request.session.get("child_profile_id")
    profile = ChildProfile.objects.filter(id=profile_id).first()
    if profile:
        return profile

    if request.user.is_authenticated:
        owned_profile = ChildProfile.objects.filter(owner=request.user).first()
        if owned_profile:
            request.session["child_profile_id"] = owned_profile.id
            request.session["selected_language"] = owned_profile.preferred_language
            return owned_profile

    profile = ChildProfile.objects.create(
        name="Little Learner",
        preferred_language="english",
    )
    request.session["child_profile_id"] = profile.id
    request.session["selected_language"] = profile.preferred_language
    return profile


def get_language_or_404(language):
    if language not in LANGUAGE_META:
        raise Http404("Unknown language mode.")
    return language


def update_profile_mastery(profile, letter_id, is_correct):
    progress, _ = LetterProgress.objects.get_or_create(profile=profile, letter_id=letter_id)
    progress.views_count += 1
    if is_correct:
        progress.correct_answers += 1
    else:
        progress.incorrect_answers += 1
    if progress.correct_answers >= max(2, progress.incorrect_answers):
        progress.completed = True
    progress.save()
    return progress


def build_questions(language, letter_pool=None, audio_first=False):
    letters = list(letter_pool or Letter.objects.filter(language=language, is_active=True))
    sample_size = min(EXERCISE_SIZE, len(letters))
    if sample_size == 0:
        return []
    chosen = random.sample(letters, sample_size)
    all_letters = list(Letter.objects.filter(language=language, is_active=True))
    questions = []
    for letter in chosen:
        distractors = [item.symbol for item in all_letters if item.id != letter.id]
        options = random.sample(distractors, min(3, len(distractors))) + [letter.symbol]
        random.shuffle(options)
        prompt = f"Listen and choose the letter for {letter.word}." if audio_first else f"Which letter matches {letter.word}?"
        questions.append(
            {
                "id": letter.id,
                "symbol": letter.symbol,
                "word": letter.word,
                "emoji": letter.emoji,
                "speech_text": letter.speech_text,
                "prompt": prompt,
                "options": options,
            }
        )
    return questions


def get_weak_letters(profile, language, limit=5):
    weak_progress = (
        profile.letter_progress.filter(letter__language=language)
        .annotate(weakness_gap=F("incorrect_answers") - F("correct_answers"))
        .filter(Q(incorrect_answers__gt=0) | Q(completed=False))
        .order_by("-weakness_gap", "-incorrect_answers", "letter__sort_order")
    )
    weak_letters = [item.letter for item in weak_progress[:limit]]
    if weak_letters:
        return weak_letters
    return list(Letter.objects.filter(language=language, is_active=True)[:limit])


def build_child_summary(child):
    attempts = child.attempts.all()
    totals = attempts.aggregate(avg_score=Avg("score"), total_attempts=Count("id"))
    weak_letters = (
        child.letter_progress.select_related("letter")
        .annotate(weakness_gap=F("incorrect_answers") - F("correct_answers"))
        .filter(incorrect_answers__gt=0)
        .order_by("-weakness_gap", "-incorrect_answers")[:5]
    )
    active_assignments = child.assignments.filter(is_active=True).select_related("teacher")[:5]
    return {
        "child": child,
        "totals": totals,
        "weak_letters": weak_letters,
        "active_assignments": active_assignments,
        "completed_letters": child.letter_progress.filter(completed=True).count(),
    }


def home(request):
    profile = get_current_profile(request)
    adult_profile = get_adult_profile(request)

    if request.method == "POST":
        action = request.POST.get("action", "save-profile")
        if action == "save-profile":
            profile.name = request.POST.get("name", profile.name).strip() or profile.name
            profile.preferred_language = request.POST.get("language", profile.preferred_language)
            profile.age_group = request.POST.get("age_group", profile.age_group).strip()
            if request.user.is_authenticated and adult_profile and adult_profile.role == "parent":
                profile.owner = request.user
            profile.save()
            request.session["selected_language"] = profile.preferred_language
            messages.success(request, "Your learning space is ready.")
            return redirect("learning:alphabet-grid", language=profile.preferred_language)
        if action == "claim-child" and request.user.is_authenticated and adult_profile and adult_profile.role == "parent":
            profile.owner = request.user
            profile.save(update_fields=["owner"])
            messages.success(request, "This learner profile is now linked to your parent account.")
            return redirect("learning:adult-report")

    selected_language = request.session.get("selected_language", profile.preferred_language)
    recent_attempt = profile.attempts.first()
    learned_count = profile.letter_progress.filter(completed=True).count()
    weak_letter_count = profile.letter_progress.filter(incorrect_answers__gt=0).count()
    context = {
        "profile": profile,
        "adult_profile": adult_profile,
        "selected_language": selected_language,
        "language_cards": LANGUAGE_META,
        "recent_attempt": recent_attempt,
        "learned_count": learned_count,
        "weak_letter_count": weak_letter_count,
        "assignment_count": profile.assignments.filter(is_active=True).count(),
        "total_letters": Letter.objects.filter(language=selected_language).count(),
    }
    return render(request, "learning/home.html", context)


def alphabet_grid(request, language):
    language = get_language_or_404(language)
    profile = get_current_profile(request)
    request.session["selected_language"] = language
    letters = Letter.objects.filter(language=language, is_active=True)
    progress_map = {
        item["letter_id"]: item
        for item in profile.letter_progress.filter(letter__language=language).values(
            "letter_id",
            "completed",
            "views_count",
            "correct_answers",
            "incorrect_answers",
        )
    }
    weak_letters = {letter.id for letter in get_weak_letters(profile, language, limit=5)}
    return render(
        request,
        "learning/alphabet_grid.html",
        {
            "profile": profile,
            "language": language,
            "language_meta": LANGUAGE_META[language],
            "letters": letters,
            "progress_map": progress_map,
            "weak_letter_ids": weak_letters,
        },
    )


def letter_detail(request, language, slug):
    language = get_language_or_404(language)
    profile = get_current_profile(request)
    letter = get_object_or_404(Letter, language=language, slug=slug, is_active=True)
    progress, _ = LetterProgress.objects.get_or_create(profile=profile, letter=letter)
    progress.views_count += 1
    progress.save(update_fields=["views_count", "last_viewed_at"])

    if request.method == "POST":
        progress.completed = True
        if progress.correct_answers < 1:
            progress.correct_answers = 1
        progress.save(update_fields=["completed", "correct_answers", "last_viewed_at"])
        messages.success(request, f"{letter.symbol} is now part of your completed letters.")
        return redirect("learning:alphabet-grid", language=language)

    siblings = list(Letter.objects.filter(language=language, is_active=True))
    current_index = siblings.index(letter)
    previous_letter = siblings[current_index - 1] if current_index > 0 else None
    next_letter = siblings[current_index + 1] if current_index < len(siblings) - 1 else None
    return render(
        request,
        "learning/letter_detail.html",
        {
            "profile": profile,
            "language": language,
            "language_meta": LANGUAGE_META[language],
            "letter": letter,
            "progress": progress,
            "previous_letter": previous_letter,
            "next_letter": next_letter,
        },
    )


def run_exercise(request, language, exercise_type, question_key, template_name):
    language = get_language_or_404(language)
    profile = get_current_profile(request)
    audio_first = exercise_type == "audio-first"

    if request.method == "POST":
        questions = request.session.get(question_key, [])
        if not questions:
            messages.error(request, "Let us start a fresh exercise round.")
            return redirect(request.path)

        score = 0
        answer_log = []
        for question in questions:
            selected = request.POST.get(f"question_{question['id']}", "")
            correct = question["symbol"]
            is_correct = selected == correct
            if is_correct:
                score += 1
            answer_log.append(
                {
                    "letter_id": question["id"],
                    "prompt": question["prompt"],
                    "correct_answer": correct,
                    "selected_answer": selected,
                    "is_correct": is_correct,
                }
            )
            update_profile_mastery(profile, question["id"], is_correct)

        stars_earned = score * 2 if exercise_type == "standard" else score * 3
        profile.stars += stars_earned
        profile.preferred_language = language
        if audio_first:
            profile.audio_first_mode = True
        profile.save(update_fields=["stars", "preferred_language", "audio_first_mode"])

        attempt = ExerciseAttempt.objects.create(
            profile=profile,
            language=language,
            exercise_type=exercise_type,
            score=score,
            total_questions=len(questions),
            answers=answer_log,
        )
        request.session.pop(question_key, None)
        messages.success(request, f"Nice work! You earned {stars_earned} stars.")
        return redirect("learning:exercise-result", attempt_id=attempt.id)

    if exercise_type == "weak-letter":
        question_pool = get_weak_letters(profile, language, limit=6)
    else:
        question_pool = None
    questions = build_questions(language, letter_pool=question_pool, audio_first=audio_first)
    request.session[question_key] = questions
    return render(
        request,
        template_name,
        {
            "profile": profile,
            "language": language,
            "language_meta": LANGUAGE_META[language],
            "questions": questions,
            "exercise_size": len(questions),
            "exercise_type": exercise_type,
        },
    )


def exercise(request, language):
    return run_exercise(request, language, "standard", "exercise_questions", "learning/exercise.html")


def weak_letter_practice(request, language):
    return run_exercise(
        request,
        language,
        "weak-letter",
        "weak_letter_questions",
        "learning/weak_letter_practice.html",
    )


def audio_first_mode(request, language):
    return run_exercise(
        request,
        language,
        "audio-first",
        "audio_first_questions",
        "learning/audio_first_mode.html",
    )


def exercise_result(request, attempt_id):
    profile = get_current_profile(request)
    attempt = get_object_or_404(ExerciseAttempt, id=attempt_id, profile=profile)
    accuracy = round((attempt.score / attempt.total_questions) * 100) if attempt.total_questions else 0
    return render(
        request,
        "learning/exercise_result.html",
        {
            "profile": profile,
            "attempt": attempt,
            "accuracy": accuracy,
            "language_meta": LANGUAGE_META[attempt.language],
        },
    )


def progress_dashboard(request):
    profile = get_current_profile(request)
    selected_language = request.session.get("selected_language", profile.preferred_language)
    letters_by_language = {
        code: Letter.objects.filter(language=code, is_active=True).count() for code in LANGUAGE_META
    }
    progress_counts = {
        code: profile.letter_progress.filter(letter__language=code, completed=True).count()
        for code in LANGUAGE_META
    }
    attempt_summary = profile.attempts.aggregate(avg_score=Avg("score"), total_attempts=Count("id"))
    recent_attempts = profile.attempts.all()[:5]
    weak_letters = get_weak_letters(profile, selected_language, limit=5)
    active_assignments = profile.assignments.filter(is_active=True).select_related("teacher")[:5]
    completion_rate = 0
    if letters_by_language.get(selected_language):
        completion_rate = round(
            (progress_counts[selected_language] / letters_by_language[selected_language]) * 100
        )

    return render(
        request,
        "learning/progress.html",
        {
            "profile": profile,
            "selected_language": selected_language,
            "letters_by_language": letters_by_language,
            "progress_counts": progress_counts,
            "attempt_summary": attempt_summary,
            "recent_attempts": recent_attempts,
            "completion_rate": completion_rate,
            "language_cards": LANGUAGE_META,
            "weak_letters": weak_letters,
            "active_assignments": active_assignments,
        },
    )


def inclusive_mode_settings(request):
    profile = get_current_profile(request)
    if request.method == "POST":
        form = AccessibilitySettingsForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Inclusive learning preferences updated.")
            return redirect("learning:inclusive-settings")
    else:
        form = AccessibilitySettingsForm(instance=profile)

    return render(
        request,
        "learning/inclusive_settings.html",
        {
            "profile": profile,
            "form": form,
        },
    )


def switch_language(request, language):
    language = get_language_or_404(language)
    profile = get_current_profile(request)
    profile.preferred_language = language
    profile.save(update_fields=["preferred_language"])
    request.session["selected_language"] = language
    return redirect("learning:alphabet-grid", language=language)


@login_required
def adult_report(request):
    adult_profile = get_adult_profile(request)
    if not adult_profile:
        return HttpResponseForbidden("Adult profile not found.")

    if adult_profile.role == "parent":
        children = ChildProfile.objects.filter(owner=request.user).prefetch_related("attempts", "letter_progress")
    else:
        child_ids = adult_profile.assignments.values_list("child_id", flat=True).distinct()
        children = ChildProfile.objects.filter(id__in=child_ids).prefetch_related("attempts", "letter_progress")

    summaries = [build_child_summary(child) for child in children]
    return render(
        request,
        "learning/adult_report.html",
        {
            "adult_profile": adult_profile,
            "child_summaries": summaries,
        },
    )


@login_required
def teacher_assignments(request):
    adult_profile = get_adult_profile(request)
    if not adult_profile or adult_profile.role != "teacher":
        return HttpResponseForbidden("Teacher access only.")

    if request.method == "POST":
        form = LessonAssignmentForm(request.POST)
        selected_language = request.POST.get("language")
        if selected_language in LANGUAGE_META:
            form.fields["letters"].queryset = Letter.objects.filter(language=selected_language, is_active=True)
        if form.is_valid():
            assignment = form.save(commit=False)
            assignment.teacher = adult_profile
            assignment.save()
            form.save_m2m()
            messages.success(request, "Lesson assignment created for the learner.")
            return redirect("learning:teacher-assignments")
    else:
        form = LessonAssignmentForm()

    assignments = adult_profile.assignments.select_related("child").prefetch_related("letters")
    return render(
        request,
        "learning/teacher_assignments.html",
        {
            "adult_profile": adult_profile,
            "form": form,
            "assignments": assignments,
        },
    )


@login_required
def select_child_profile(request, child_id):
    child = get_object_or_404(ChildProfile, id=child_id)
    adult_profile = get_adult_profile(request)
    has_access = False
    if request.user == child.owner:
        has_access = True
    elif adult_profile and adult_profile.role == "teacher":
        has_access = adult_profile.assignments.filter(child=child).exists()

    if not has_access:
        return HttpResponseForbidden("You do not have access to this learner.")

    request.session["child_profile_id"] = child.id
    request.session["selected_language"] = child.preferred_language
    messages.success(request, f"Now viewing {child.name}'s learning profile.")
    return redirect("learning:progress")


def sign_up(request):
    if request.user.is_authenticated:
        return redirect("learning:adult-report")

    if request.method == "POST":
        form = AdultSignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.email = form.cleaned_data["email"]
            user.save()
            AdultProfile.objects.create(
                user=user,
                role=form.cleaned_data["role"],
                display_name=form.cleaned_data["display_name"],
                organization=form.cleaned_data["organization"],
            )
            login(request, user)
            messages.success(request, "Your adult account is ready.")
            return redirect("learning:adult-report")
    else:
        form = AdultSignUpForm()

    return render(request, "learning/auth/sign_up.html", {"form": form})


def sign_in(request):
    if request.user.is_authenticated:
        return redirect("learning:adult-report")

    if request.method == "POST":
        form = AdultLoginForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            messages.success(request, "Signed in successfully.")
            return redirect("learning:adult-report")
    else:
        form = AdultLoginForm(request)

    return render(request, "learning/auth/sign_in.html", {"form": form})


@login_required
def sign_out(request):
    logout(request)
    messages.success(request, "Signed out successfully.")
    return redirect("learning:home")
