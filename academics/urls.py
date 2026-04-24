from django.urls import path

from . import views

app_name = "academics"

urlpatterns = [
    path("", views.academic_home, name="home"),
    path("marks/new/", views.mark_create, name="mark-create"),
    path("marks/<int:pk>/<str:status>/", views.verify_mark, name="mark-verify"),
    path("syllabus/new/", views.syllabus_create, name="syllabus-create"),
    path("activities/new/", views.activity_create, name="activity-create"),
    path("exams/new/", views.exam_create, name="exam-create"),
    path("grades/new/", views.grade_create, name="grade-create"),
]
