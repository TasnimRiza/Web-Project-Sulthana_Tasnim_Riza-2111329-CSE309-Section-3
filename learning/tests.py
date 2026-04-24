from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import AdultProfile, ChildProfile, ExerciseAttempt, LessonAssignment, Letter, LetterProgress


class LearningFlowTests(TestCase):
    def setUp(self):
        self.parent_user = User.objects.create_user(username="parent1", password="StrongPass123")
        self.teacher_user = User.objects.create_user(username="teacher1", password="StrongPass123")
        self.parent_profile = AdultProfile.objects.create(
            user=self.parent_user,
            role="parent",
            display_name="Parent One",
        )
        self.teacher_profile = AdultProfile.objects.create(
            user=self.teacher_user,
            role="teacher",
            display_name="Teacher One",
            organization="Sunny School",
        )
        self.child = ChildProfile.objects.create(
            name="Nila",
            preferred_language="english",
            owner=self.parent_user,
        )
        self.english_letter = Letter.objects.filter(language="english").first()

    def attach_child_session(self):
        session = self.client.session
        session["child_profile_id"] = self.child.id
        session["selected_language"] = self.child.preferred_language
        session.save()

    def test_home_page_loads(self):
        response = self.client.get(reverse("learning:home"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Shobdo & Letters")

    def test_seeded_letters_exist(self):
        self.assertTrue(Letter.objects.filter(language="english").exists())
        self.assertTrue(Letter.objects.filter(language="bangla").exists())

    def test_exercise_submission_creates_attempt(self):
        self.attach_child_session()
        response = self.client.get(reverse("learning:exercise", kwargs={"language": "english"}))
        self.assertEqual(response.status_code, 200)
        session = self.client.session
        questions = session.get("exercise_questions", [])
        payload = {f"question_{question['id']}": question["symbol"] for question in questions}
        post_response = self.client.post(
            reverse("learning:exercise", kwargs={"language": "english"}),
            payload,
        )
        self.assertEqual(post_response.status_code, 302)
        self.assertEqual(ExerciseAttempt.objects.count(), 1)
        attempt = ExerciseAttempt.objects.first()
        self.assertEqual(attempt.score, len(questions))

    def test_progress_page_loads(self):
        self.attach_child_session()
        response = self.client.get(reverse("learning:progress"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Progress Dashboard")

    def test_weak_letter_practice_records_incorrect_answers(self):
        self.attach_child_session()
        progress = LetterProgress.objects.create(profile=self.child, letter=self.english_letter, incorrect_answers=2)
        response = self.client.get(reverse("learning:weak-letter-practice", kwargs={"language": "english"}))
        self.assertEqual(response.status_code, 200)
        session = self.client.session
        questions = session.get("weak_letter_questions", [])
        self.assertTrue(questions)
        payload = {f"question_{question['id']}": "wrong" for question in questions}
        self.client.post(reverse("learning:weak-letter-practice", kwargs={"language": "english"}), payload)
        progress.refresh_from_db()
        self.assertGreaterEqual(progress.incorrect_answers, 2)

    def test_parent_report_shows_owned_child(self):
        self.client.force_login(self.parent_user)
        response = self.client.get(reverse("learning:adult-report"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Nila")

    def test_teacher_can_create_assignment(self):
        self.client.force_login(self.teacher_user)
        response = self.client.post(
            reverse("learning:teacher-assignments"),
            {
                "child": self.child.id,
                "language": "english",
                "title": "Focus on A to E",
                "note": "Practice these at home.",
                "letters": [self.english_letter.id],
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(LessonAssignment.objects.count(), 1)

    def test_inclusive_settings_update_profile(self):
        self.attach_child_session()
        response = self.client.post(
            reverse("learning:inclusive-settings"),
            {
                "inclusive_mode": "on",
                "audio_first_mode": "on",
                "high_contrast_mode": "on",
                "large_text_mode": "on",
                "simplified_layout": "on",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.child.refresh_from_db()
        self.assertTrue(self.child.inclusive_mode)
        self.assertTrue(self.child.audio_first_mode)
