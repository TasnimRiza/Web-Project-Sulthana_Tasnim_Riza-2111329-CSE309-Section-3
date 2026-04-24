from django.contrib import admin

from .models import UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "role", "school", "upazila", "phone")
    list_filter = ("role", "school", "upazila")
    search_fields = ("user__username", "user__first_name", "user__last_name", "phone")

# Register your models here.
