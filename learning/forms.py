from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User

from .models import ChildProfile, LessonAssignment, Letter


class AdultSignUpForm(UserCreationForm):
    ROLE_CHOICES = [
        ("parent", "Parent"),
        ("teacher", "Teacher"),
    ]

    email = forms.EmailField(required=True)
    role = forms.ChoiceField(choices=ROLE_CHOICES)
    display_name = forms.CharField(max_length=100)
    organization = forms.CharField(max_length=120, required=False)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "email", "display_name", "role", "organization")


class AdultLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Username"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Password"}))


class AccessibilitySettingsForm(forms.ModelForm):
    class Meta:
        model = ChildProfile
        fields = [
            "inclusive_mode",
            "audio_first_mode",
            "high_contrast_mode",
            "large_text_mode",
            "simplified_layout",
        ]
        widgets = {field: forms.CheckboxInput() for field in fields}
        labels = {
            "inclusive_mode": "Turn on inclusive learning support",
            "audio_first_mode": "Use audio-first learning",
            "high_contrast_mode": "Enable high contrast",
            "large_text_mode": "Use larger text",
            "simplified_layout": "Use simplified layout",
        }
        help_texts = {
            "inclusive_mode": "Activates a support-focused experience for diverse learning needs.",
            "audio_first_mode": "Gives listening cues more priority than text-heavy prompts.",
            "high_contrast_mode": "Improves visibility for children who need stronger color contrast.",
            "large_text_mode": "Makes letters and labels easier to read.",
            "simplified_layout": "Reduces visual clutter and keeps the page calmer.",
        }


class LessonAssignmentForm(forms.ModelForm):
    child = forms.ModelChoiceField(queryset=ChildProfile.objects.all())
    letters = forms.ModelMultipleChoiceField(
        queryset=Letter.objects.filter(is_active=True),
        required=False,
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = LessonAssignment
        fields = ["child", "language", "title", "note", "due_date", "letters"]
        widgets = {
            "due_date": forms.DateInput(attrs={"type": "date"}),
            "note": forms.Textarea(attrs={"rows": 4}),
        }


class ChildProfileForm(forms.ModelForm):
    class Meta:
        model = ChildProfile
        fields = ["name", "age_group", "preferred_language"]
