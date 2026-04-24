# School Monitoring and Management System (SMMS)

SMMS is a Django full-stack web application for rural primary school monitoring and management. It adds role-based portals for Teacher, EduKids Student/Guardian, Head Teacher, UEO, and Admin users.

## Features

- Django authentication with `UserProfile` roles.
- School, class, section, subject, and academic-year setup.
- Student, guardian, profile, enrollment, and document upload management.
- Daily attendance with head-teacher verification and low-attendance alerts below 75%.
- Marks, grades, ranking, syllabus progress, and class activity logging.
- Teacher leave requests with head-teacher approval/rejection.
- Stipend eligibility using attendance >= 85% and GPA >= 3.80.
- Notices, internal messages, UEO inspections, evidence uploads, interventions.
- AI-ready quiz generation with OpenAI API fallback to a local question bank.
- Role dashboards, CSV reports, and audit logs.

## Setup

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_smms
python manage.py runserver
```

Open `http://127.0.0.1:8000/`.

Sample users created by `seed_smms`:

- `admin`
- `headteacher`
- `teacher`
- `student`
- `guardian`
- `ueo`

All sample passwords are `password123`.

## Production Notes

SQLite is used by default for development. For PostgreSQL, set `DATABASE_URL`, `SECRET_KEY`, and hosting environment variables. Static files are configured with WhiteNoise. Set `OPENAI_API_KEY` and optionally `OPENAI_MODEL` to enable live AI quiz generation.
