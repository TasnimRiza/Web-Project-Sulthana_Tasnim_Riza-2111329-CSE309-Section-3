from datetime import date

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from accounts.models import UserProfile
from academics.models import Exam, Grade, Mark
from attendance.models import Attendance, AttendanceRecord
from schools.models import AcademicYear, ClassRoom, School, Section, Subject
from students.models import Enrollment, Guardian, Student, StudentProfile


class Command(BaseCommand):
    help = "Create sample SMMS users, school setup, students, attendance, and marks."

    def handle(self, *args, **options):
        admin = self.user("admin", "Admin", "Admin", True)
        head = self.user("headteacher", "Head", "HeadTeacher")
        teacher = self.user("teacher", "Teacher", "Teacher")
        ueo = self.user("ueo", "UEO", "UEO")
        guardian_user = self.user("guardian", "Guardian", "Guardian")
        student_user = self.user("student", "Student", "Student")

        school, _ = School.objects.get_or_create(
            code="SMMS-001",
            defaults={"name": "Shapla Rural Primary School", "upazila": "Savar", "district": "Dhaka", "head_teacher": head, "ueo": ueo},
        )
        for user in [head, teacher, ueo, guardian_user, student_user]:
            profile = user.smms_profile
            profile.school = school
            profile.upazila = school.upazila
            profile.save()

        year, _ = AcademicYear.objects.get_or_create(name="2026", defaults={"starts_on": date(2026, 1, 1), "ends_on": date(2026, 12, 31), "is_current": True})
        classroom, _ = ClassRoom.objects.get_or_create(school=school, name="Class 4", defaults={"numeric_level": 4, "class_teacher": teacher})
        section, _ = Section.objects.get_or_create(classroom=classroom, name="A")
        subject, _ = Subject.objects.get_or_create(school=school, code="BAN-4", defaults={"name": "Bangla"})
        subject.teachers.add(teacher)
        subject.classrooms.add(classroom)

        guardian, _ = Guardian.objects.get_or_create(user=guardian_user, defaults={"name": "Amina Begum", "phone": "01700000000"})
        student, _ = Student.objects.get_or_create(
            user=student_user,
            student_id="STU-001",
            defaults={"name": "Rafi Hasan", "school": school, "guardian": guardian, "admission_date": date(2026, 1, 5)},
        )
        StudentProfile.objects.get_or_create(student=student)
        Enrollment.objects.get_or_create(student=student, academic_year=year, classroom=classroom, section=section, defaults={"roll_number": 1})

        for letter, low, high, point in [("A+", 80, 100, 5), ("A", 70, 79, 4), ("A-", 60, 69, 3.5), ("B", 50, 59, 3), ("C", 40, 49, 2), ("F", 0, 39, 0)]:
            Grade.objects.get_or_create(letter=letter, defaults={"min_score": low, "max_score": high, "point": point})
        exam, _ = Exam.objects.get_or_create(name="Half Yearly", academic_year=year)
        Mark.objects.get_or_create(student=student, subject=subject, exam=exam, defaults={"written": 72, "oral": 10, "practical": 0, "submitted_by": teacher, "verification_status": "Verified", "verified_by": head})

        sheet, _ = Attendance.objects.get_or_create(classroom=classroom, section=section, date=date(2026, 4, 25), defaults={"taken_by": teacher, "verification_status": "Verified", "verified_by": head})
        AttendanceRecord.objects.get_or_create(attendance=sheet, student=student, defaults={"status": "Present"})
        self.stdout.write(self.style.SUCCESS("SMMS sample data created. Login password for sample users is: password123"))

    def user(self, username, first_name, role, superuser=False):
        user, created = User.objects.get_or_create(username=username, defaults={"first_name": first_name, "is_staff": superuser, "is_superuser": superuser})
        user.set_password("password123")
        if not user.first_name:
            user.first_name = first_name
        user.is_staff = user.is_staff or superuser
        user.is_superuser = user.is_superuser or superuser
        user.save()
        profile, _ = UserProfile.objects.get_or_create(user=user)
        profile.role = role
        profile.save()
        return user
