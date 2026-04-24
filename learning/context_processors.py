from .models import AdultProfile, ChildProfile


def learning_preferences(request):
    profile = None
    classes = []
    adult_profile = None
    profile_id = request.session.get("child_profile_id")
    if profile_id:
        profile = ChildProfile.objects.filter(id=profile_id).first()

    if request.user.is_authenticated:
        adult_profile = AdultProfile.objects.filter(user=request.user).first()

    if profile:
        if profile.inclusive_mode:
            classes.append("inclusive-mode")
        if profile.high_contrast_mode:
            classes.append("high-contrast-mode")
        if profile.large_text_mode:
            classes.append("large-text-mode")
        if profile.simplified_layout:
            classes.append("simplified-layout")
        if profile.audio_first_mode:
            classes.append("audio-first-mode")

    return {
        "active_child_profile": profile,
        "accessibility_classes": " ".join(classes),
        "adult_session_profile": adult_profile,
    }
