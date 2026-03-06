# grievances/urls.py

from django.urls import path, include
from . import views

app_name = 'grievances'

urlpatterns = [
    # ========================================
    # HOME & AUTHENTICATION
    # ========================================
    path('', views.home, name='home'),
    path('register/', views.user_register, name='register'),
    path('login/', views.user_login, name='user_login'),
    path('logout/', views.user_logout, name='user_logout'),
  

    
    # ========================================
    # DASHBOARDS (Role-based)
    # ========================================
    path('student/dashboard/', views.student_dashboard, name='student_dashboard'),
    path('staff/dashboard/', views.staff_dashboard, name='staff_dashboard'),
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    
    # ========================================
    # SERVICE REQUESTS
    # ========================================
    path('requests/new/', views.submit_request, name='submit_request'),
    path('requests/', views.my_requests, name='my_requests'),
    path('requests/<int:pk>/', views.request_detail, name='request_detail'),
    path('requests/<int:pk>/update/', views.update_request_status, name='update_request_status'),
    path('requests/<int:pk>/assign/', views.assign_request_to_self, name='assign_request_to_self'),
    
    # ========================================
    # STAFF REQUEST MANAGEMENT
    # ========================================
    path('staff/requests/', views.staff_requests_list, name='staff_requests_list'),
    
    # ========================================
    # ANNOUNCEMENTS
    # ========================================
    path('announcements/', views.announcements_list, name='announcements_list'),
    path('announcements/<int:pk>/', views.announcement_detail, name='announcement_detail'),
    path('announcements/create/', views.create_announcement, name='create_announcement'),
    
    # ========================================
    # NOTIFICATIONS
    # ========================================
    path('notifications/', views.notifications_list, name='notifications_list'),
    path('notifications/<int:pk>/read/', views.mark_notification_read, name='mark_notification_read'),
    path('notifications/mark-all-read/', views.mark_all_notifications_read, name='mark_all_notifications_read'),
    
    # ========================================
    # FEEDBACK
    # ========================================
    path('feedback/new/', views.submit_feedback, name='submit_feedback'),
    
    # ========================================
    # PROFILE
    # ========================================
    path('profile/', views.user_profile, name='user_profile'),
    
    # ========================================
    # ADMIN FEATURES
    # ========================================
    path('admin/audit-logs/', views.view_audit_logs, name='view_audit_logs'),
    
    # ========================================
    # API ENDPOINTS (AJAX)
    # ========================================
    path('api/notifications/count/', views.get_unread_notifications_count, name='api_notification_count'),
]