from django.urls import path

from . import views

app_name = "students"

urlpatterns = [
    path("", views.student_list, name="list"),
    path("new/", views.student_create, name="create"),
    path("guardians/new/", views.guardian_create, name="guardian-create"),
    path("enrollments/new/", views.enrollment_create, name="enrollment-create"),
    path("<int:pk>/", views.student_detail, name="detail"),
]
