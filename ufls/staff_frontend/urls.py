from django.contrib.auth import views as auth_views
from django.urls import include, path

from staff_frontend import views

app_name = "staff_frontend"

urlpatterns = [
    path("", views.index, name="index"),
    path("app/", views.application, name="application"),
    path("distribute/apps/", views.distributeApps, name="distribute"),
    path('distribute/apps/license/<str:program_key>/', views.checkAndDistribute, name='check-and-distribute'),
    path("api/staff/<str:email>/", views.getStaffAssignments, name="get-staff-assignments"),
    path("open/", views.open, name="open"),
    path("open/apply/<str:openpk>/", views.application, name="open-apply"),
    path("help/", views.help, name="help"),
    path("portal/", views.dashboard, name="portal"),
    path("hr/", views.hr, name="hr"),
    path("hr/app/<str:id>/", views.hrAppView, name="hr-app-view"),
    path("ufls/staff/", views.uflsStaffAuthentication, name="ufls-staff-return"),
    path("ufls/login/", views.uflsLogin, name="ufls-login"),
    path("staff/", views.staffList, name="staff-list"),
    path("departments/", views.departmentList, name="departments"),
    path("department/<str:pk>/", views.departmentView, name="department"),
    path("department/<str:pk>/newTask/", views.newTask, name="new-department-task"),
    path(
        "department/<str:pk>/newAnnouncement/",
        views.newAnnouncement,
        name="new-department-announcement",
    ),
    path("task/<str:pk>/", views.staffTaskView, name="staff-task"),
    path("task/<str:pk>/done/", views.markStaffTaskDone, name="mark-staff-task-done"),
]
