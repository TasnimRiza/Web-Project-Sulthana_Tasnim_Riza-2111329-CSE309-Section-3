from django.urls import path

from . import views

app_name = "schools"

urlpatterns = [
    path("", views.schools, name="schools"),
    path("setup/", views.setup, name="setup"),
    path("new/", views.school_create, name="school-create"),
    path("academic-years/new/", views.academic_year_create, name="academic-year-create"),
    path("classes/new/", views.classroom_create, name="classroom-create"),
    path("sections/new/", views.section_create, name="section-create"),
    path("subjects/new/", views.subject_create, name="subject-create"),
]
