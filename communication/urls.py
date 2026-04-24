from django.urls import path

from . import views

app_name = "communication"

urlpatterns = [
    path("notices/", views.notices, name="notices"),
    path("notices/new/", views.notice_create, name="notice-create"),
    path("messages/", views.messages, name="messages"),
    path("messages/new/", views.message_create, name="message-create"),
]
