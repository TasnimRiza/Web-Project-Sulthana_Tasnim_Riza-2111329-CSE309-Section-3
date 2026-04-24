from django.urls import path

from . import views

app_name = "learning"

urlpatterns = [
    path("", views.home, name="home"),
    path("auth/sign-up/", views.sign_up, name="sign-up"),
    path("auth/sign-in/", views.sign_in, name="sign-in"),
    path("auth/sign-out/", views.sign_out, name="sign-out"),
    path("progress/", views.progress_dashboard, name="progress"),
    path("reports/", views.adult_report, name="adult-report"),
    path("teacher/assignments/", views.teacher_assignments, name="teacher-assignments"),
    path("children/select/<int:child_id>/", views.select_child_profile, name="select-child"),
    path("settings/inclusive/", views.inclusive_mode_settings, name="inclusive-settings"),
    path("switch/<str:language>/", views.switch_language, name="switch-language"),
    path("learn/<str:language>/", views.alphabet_grid, name="alphabet-grid"),
    path("learn/<str:language>/<slug:slug>/", views.letter_detail, name="letter-detail"),
    path("exercise/<str:language>/", views.exercise, name="exercise"),
    path("practice/weak/<str:language>/", views.weak_letter_practice, name="weak-letter-practice"),
    path("practice/audio-first/<str:language>/", views.audio_first_mode, name="audio-first-mode"),
    path("exercise/result/<int:attempt_id>/", views.exercise_result, name="exercise-result"),
]
