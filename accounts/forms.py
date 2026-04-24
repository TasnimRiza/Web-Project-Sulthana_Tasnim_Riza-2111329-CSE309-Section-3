from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import UserProfile


class SMMSUserCreationForm(UserCreationForm):
    role = forms.ChoiceField(choices=UserProfile.ROLE_CHOICES)
    school = forms.ModelChoiceField(queryset=UserProfile._meta.get_field("school").remote_field.model.objects.all(), required=False)

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email", "role", "school", "password1", "password2")

    def save(self, commit=True):
        user = super().save(commit=commit)
        profile, _ = UserProfile.objects.get_or_create(user=user)
        profile.role = self.cleaned_data["role"]
        profile.school = self.cleaned_data.get("school")
        if commit:
            profile.save()
        return user


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ("role", "school", "upazila", "phone", "address", "photo")
