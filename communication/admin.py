from django.contrib import admin

from .models import Message, Notice


admin.site.register(Notice)
admin.site.register(Message)

# Register your models here.
