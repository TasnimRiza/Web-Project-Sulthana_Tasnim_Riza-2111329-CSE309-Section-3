from django.urls import path

from . import views

app_name = "attendance"

urlpatterns = [
    path("", views.attendance_list, name="list"),
    path("take/", views.take_attendance, name="take"),
    path("<int:pk>/<str:status>/", views.verify_attendance, name="verify"),
]
