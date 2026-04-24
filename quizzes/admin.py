from django.contrib import admin

from .models import Quiz, QuizAttempt, QuizQuestion, Reward


admin.site.register(Quiz)
admin.site.register(QuizQuestion)
admin.site.register(QuizAttempt)
admin.site.register(Reward)

# Register your models here.
