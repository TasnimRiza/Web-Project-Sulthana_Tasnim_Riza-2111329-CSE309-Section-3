from django.urls import path

from . import views

app_name = "stipend"

urlpatterns = [
    path("", views.stipend_list, name="list"),
    path("new/", views.stipend_create, name="create"),
    path("<int:pk>/validate/", views.validate_stipend, name="validate"),
]
