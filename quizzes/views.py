from django.shortcuts import redirect, render

from accounts.decorators import role_required
from audit.models import log_action
from schools.models import Subject
from students.models import Student

from .forms import QuizGenerateForm
from .models import Quiz, QuizQuestion, Reward
from .services import generate_questions


@role_required("Student", "Guardian", "Teacher", "Admin")
def quiz_list(request):
    quizzes = Quiz.objects.select_related("student", "subject").prefetch_related("questions", "attempts")
    return render(request, "quizzes/list.html", {"quizzes": quizzes})


@role_required("Student", "Teacher", "Admin")
def quiz_create(request):
    student = getattr(request.user, "student_record", None) or Student.objects.first()
    form = QuizGenerateForm(request.POST or None, subject_queryset=Subject.objects.all())
    if form.is_valid() and student:
        subject = form.cleaned_data["subject"]
        quiz = Quiz.objects.create(
            student=student,
            subject=subject,
            chapter=form.cleaned_data["chapter"],
            generated_by_ai=form.cleaned_data["use_ai"],
        )
        for item in generate_questions(subject.name, quiz.chapter):
            QuizQuestion.objects.create(quiz=quiz, **item)
        log_action(request.user, "generated quiz", quiz, request=request)
        return redirect("quizzes:list")
    return render(request, "smms/form.html", {"form": form, "title": "Generate Quiz"})


@role_required("Student", "Admin")
def award_reward(request, quiz_id):
    quiz = Quiz.objects.get(pk=quiz_id)
    Reward.objects.create(student=quiz.student, title=f"{quiz.subject} quiz completed", points=10)
    return redirect("quizzes:list")

# Create your views here.
