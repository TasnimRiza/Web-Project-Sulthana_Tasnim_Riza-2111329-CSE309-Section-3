from django.shortcuts import redirect, render

from accounts.decorators import role_required
from audit.models import log_action

from .forms import MessageForm, NoticeForm
from .models import Message, Notice


@role_required("Teacher", "Student", "Guardian", "HeadTeacher", "UEO", "Admin")
def notices(request):
    profile = request.user.smms_profile
    items = Notice.objects.filter(is_published=True)
    items = items.filter(target_role__in=["All", profile.role])
    if profile.school:
        items = items.filter(school__isnull=True) | items.filter(school=profile.school)
    return render(request, "communication/notices.html", {"notices": items.distinct()})


@role_required("HeadTeacher", "Admin")
def notice_create(request):
    form = NoticeForm(request.POST or None)
    if form.is_valid():
        notice = form.save(commit=False)
        notice.published_by = request.user
        notice.save()
        log_action(request.user, "published notice", notice, request=request)
        return redirect("communication:notices")
    return render(request, "smms/form.html", {"form": form, "title": "Publish Notice"})


@role_required("Teacher", "Student", "Guardian", "HeadTeacher", "UEO", "Admin")
def messages(request):
    inbox = Message.objects.filter(recipient=request.user).select_related("sender")
    return render(request, "communication/messages.html", {"messages": inbox})


@role_required("Teacher", "Student", "Guardian", "HeadTeacher", "UEO", "Admin")
def message_create(request):
    form = MessageForm(request.POST or None)
    if form.is_valid():
        message = form.save(commit=False)
        message.sender = request.user
        message.save()
        log_action(request.user, "sent message", message, request=request)
        return redirect("communication:messages")
    return render(request, "smms/form.html", {"form": form, "title": "Send Message"})

# Create your views here.
