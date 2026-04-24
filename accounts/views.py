from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordResetView
from django.urls import reverse_lazy
from django.shortcuts import redirect, render

from .decorators import role_required
from .forms import SMMSUserCreationForm, UserProfileForm


class SMMSLoginView(LoginView):
    template_name = "accounts/login.html"


class SMMSLogoutView(LogoutView):
    pass


class SMMSPasswordChangeView(PasswordChangeView):
    template_name = "accounts/password_change.html"
    success_url = reverse_lazy("dashboards:home")


class SMMSPasswordResetView(PasswordResetView):
    template_name = "accounts/password_reset.html"
    success_url = reverse_lazy("accounts:login")


@role_required("Admin", "HeadTeacher")
def register_user(request):
    if request.method == "POST":
        form = SMMSUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("accounts:user-list")
    else:
        form = SMMSUserCreationForm()
    return render(request, "smms/form.html", {"form": form, "title": "Create User"})


@login_required
def profile(request):
    profile = request.user.smms_profile
    if request.method == "POST":
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect("accounts:profile")
    else:
        form = UserProfileForm(instance=profile)
    return render(request, "smms/form.html", {"form": form, "title": "My Profile"})


@role_required("Admin", "HeadTeacher")
def user_list(request):
    from django.contrib.auth.models import User

    users = User.objects.select_related("smms_profile").order_by("username")
    return render(request, "smms/list.html", {"title": "Users", "objects": users, "columns": ["username", "email", "is_active"]})

# Create your views here.
