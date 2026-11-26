
from django.contrib import admin
from django.urls import path
from manager import views

urlpatterns = [
    path("django-admin/", admin.site.urls),
    path("", views.dashboard, name="dashboard"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("classes/", views.classes_view, name="classes"),
    path("students/", views.students_view, name="students"),
    path("subjects/", views.subjects_view, name="subjects"),
    path("tests/", views.tests_view, name="tests"),
    path("marks/<int:test_id>/", views.marks_view, name="marks"),
    path("results/", views.results_view, name="results"),
]
