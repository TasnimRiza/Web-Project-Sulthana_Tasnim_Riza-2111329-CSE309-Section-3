from functools import wraps

from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied


def user_role(user):
    if user.is_superuser:
        return "Admin"
    profile = getattr(user, "smms_profile", None)
    return profile.role if profile else None


def role_required(*roles):
    def decorator(view_func):
        @login_required
        @wraps(view_func)
        def wrapped(request, *args, **kwargs):
            role = user_role(request.user)
            if role in roles or role == "Admin":
                return view_func(request, *args, **kwargs)
            raise PermissionDenied

        return wrapped

    return decorator
