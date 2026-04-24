from django import forms

from .models import Message, Notice


class NoticeForm(forms.ModelForm):
    class Meta:
        model = Notice
        fields = ("title", "body", "school", "target_role", "is_published")


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ("recipient", "subject", "body")
