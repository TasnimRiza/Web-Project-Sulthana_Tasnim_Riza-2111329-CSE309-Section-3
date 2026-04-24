from django.urls import path

from . import views

app_name = "leave_management"

urlpatterns = [
    path("", views.leave_list, name="list"),
    path("new/", views.leave_create, name="create"),
    path("<int:pk>/<str:status>/", views.review_leave, name="review"),
]
