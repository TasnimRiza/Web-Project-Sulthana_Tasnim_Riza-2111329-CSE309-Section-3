from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="ChildProfile",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(default="Little Learner", max_length=80)),
                ("age_group", models.CharField(blank=True, max_length=20)),
                ("preferred_language", models.CharField(default="english", max_length=20)),
                ("stars", models.PositiveIntegerField(default=0)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name="Letter",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("language", models.CharField(choices=[("english", "English"), ("bangla", "Bangla")], max_length=20)),
                ("symbol", models.CharField(max_length=10)),
                ("slug", models.SlugField(blank=True, max_length=120, unique=True)),
                ("name", models.CharField(max_length=50)),
                ("transliteration", models.CharField(blank=True, max_length=50)),
                ("word", models.CharField(max_length=100)),
                ("word_translation", models.CharField(blank=True, max_length=120)),
                ("emoji", models.CharField(blank=True, max_length=10)),
                ("description", models.CharField(max_length=255)),
                ("speech_text", models.CharField(max_length=120)),
                ("sort_order", models.PositiveIntegerField(default=0)),
                ("is_active", models.BooleanField(default=True)),
            ],
            options={"ordering": ["sort_order", "symbol"], "unique_together": {("language", "symbol")}},
        ),
        migrations.CreateModel(
            name="ExerciseAttempt",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("language", models.CharField(max_length=20)),
                ("score", models.PositiveIntegerField(default=0)),
                ("total_questions", models.PositiveIntegerField(default=5)),
                ("answers", models.JSONField(blank=True, default=list)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("profile", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="attempts", to="learning.childprofile")),
            ],
            options={"ordering": ["-created_at"]},
        ),
        migrations.CreateModel(
            name="LetterProgress",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("views_count", models.PositiveIntegerField(default=0)),
                ("completed", models.BooleanField(default=False)),
                ("last_viewed_at", models.DateTimeField(auto_now=True)),
                ("letter", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="progress_items", to="learning.letter")),
                ("profile", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="letter_progress", to="learning.childprofile")),
            ],
            options={"unique_together": {("profile", "letter")}},
        ),
    ]
