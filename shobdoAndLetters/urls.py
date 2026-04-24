from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("dashboards.urls")),
    path("accounts/", include("accounts.urls")),
    path("schools/", include("schools.urls")),
    path("students/", include("students.urls")),
    path("attendance/", include("attendance.urls")),
    path("academics/", include("academics.urls")),
    path("leave/", include("leave_management.urls")),
    path("stipend/", include("stipend.urls")),
    path("communication/", include("communication.urls")),
    path("inspections/", include("inspections.urls")),
    path("quizzes/", include("quizzes.urls")),
    path("reports/", include("reports.urls")),
    path("audit/", include("audit.urls")),
    path("learning/", include("learning.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
