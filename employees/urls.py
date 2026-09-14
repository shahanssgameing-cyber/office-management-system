from django.urls import path
from . import views

urlpatterns = [
    path("", views.employee_list, name="employee_list"),
    path("add/", views.employee_add, name="employee_add"),
    path("edit/<int:id>/", views.employee_edit, name="employee_edit"),
    path("delete/<int:id>/", views.employee_delete, name="employee_delete"),
    path("login/", views.user_login, name="user_login"),
    path("logout/", views.user_logout, name="user_logout"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("attendance/", views.attendance_list, name="attendance_list"),
    path("attendance/add/", views.attendance_add, name="attendance_add"),
    path("salary/", views.salary_list, name="salary_list"),
    path("salary/add/", views.salary_add, name="salary_add"),
    path("api/employees/", views.employee_api, name="employee_api"),
]