from django.urls import path

from . import views

app_name = "accounts"

urlpatterns = [
    path("login/", views.SMMSLoginView.as_view(), name="login"),
    path("logout/", views.SMMSLogoutView.as_view(), name="logout"),
    path("register/", views.register_user, name="register"),
    path("profile/", views.profile, name="profile"),
    path("users/", views.user_list, name="user-list"),
    path("password/change/", views.SMMSPasswordChangeView.as_view(), name="password-change"),
    path("password/reset/", views.SMMSPasswordResetView.as_view(), name="password-reset"),
]
