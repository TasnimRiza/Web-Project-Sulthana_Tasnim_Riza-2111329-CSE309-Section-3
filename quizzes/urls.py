from django.urls import path

from . import views

app_name = "quizzes"

urlpatterns = [
    path("", views.quiz_list, name="list"),
    path("new/", views.quiz_create, name="create"),
    path("<int:quiz_id>/reward/", views.award_reward, name="reward"),
]
