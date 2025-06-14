from django.urls import path
from . import views # Import views from your current app

app_name = "students" # Define the application namespace [32, 34]

urlpatterns = [
    # URL for the main student dashboard
    path("dashboard/", views.StudentDashboardView.as_view(), name="student_dashboard"),
    
    # URL for a specific session's details
    path("sessions/<int:pk>/", views.SessionDetailView.as_view(), name="session_detail"),
    
    # URL to handle actions on sessions (e.g., cancel, join, reschedule)
    # <str:action> captures the action keyword (e.g., 'cancel', 'join')
    path("sessions/<int:pk>/<str:action>/", views.SessionActionView.as_view(), name="session_action"),
]