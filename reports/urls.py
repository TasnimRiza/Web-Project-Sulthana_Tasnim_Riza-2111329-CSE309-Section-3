from django.urls import path

from . import views

app_name = "reports"

urlpatterns = [
    path("", views.report_center, name="center"),
    path("attendance.csv", views.attendance_csv, name="attendance-csv"),
    path("marks.csv", views.marks_csv, name="marks-csv"),
    path("stipends.csv", views.stipend_csv, name="stipend-csv"),
    path("inspections.csv", views.inspection_csv, name="inspection-csv"),
    path("progress.csv", views.progress_csv, name="progress-csv"),
]
