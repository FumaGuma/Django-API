from django.urls import path, include
from admissions import views
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

router = DefaultRouter()
router.register(r"users", views.UserViewSet, basename="users")


urlpatterns = [
    path("", include(router.urls)),
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("students/", views.Students.as_view(), name="students_list"),
    path("admins/", views.Admins.as_view(), name="admins"),
    path("admins/<int:pk>", views.Admins.as_view(), name="delete_admin"),
    path("majors/", views.Majors.as_view(), name="majors_overview_list"),
    path("majors/<int:pk>", views.Majors.as_view(), name="delete_major"),
    path("subjects/", views.Subjects.as_view(), name="subject_list"),
    path("applications/", views.Applications.as_view(), name="applications"),
    path("approvals/", views.Approvals.as_view(), name="approvals"),
]
