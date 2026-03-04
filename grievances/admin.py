# grievances/admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import (
    User, Department, ServiceRequest, Announcement,
    Notification, Feedback, AcademicResource, AuditLog
)

# ========================================
# CUSTOM USER ADMIN
# ========================================

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Enhanced admin for custom User model"""
    list_display = ['email', 'full_name', 'role', 'is_active', 'date_joined']
    list_filter = ['role', 'is_active', 'is_staff']
    search_fields = ['email', 'full_name', 'student_id', 'staff_id']
    ordering = ['-date_joined']
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('full_name', 'username', 'phone')}),
        ('Role & Status', {'fields': ('role', 'is_active', 'is_staff', 'is_superuser')}),
        ('Student Info', {'fields': ('student_id', 'admission_number', 'year_of_study')}),
        ('Staff Info', {'fields': ('staff_id', 'designation')}),
        ('Preferences', {'fields': ('email_notifications', 'in_app_notifications')}),
        ('Dates', {'fields': ('last_login', 'date_joined')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'full_name', 'role', 'password1', 'password2'),
        }),
    )


# ========================================
# DEPARTMENT ADMIN
# ========================================

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['dept_code', 'dept_name', 'head_name', 'email', 'phone']
    search_fields = ['dept_code', 'dept_name', 'head_name']
    ordering = ['dept_name']


# ========================================
# SERVICE REQUEST ADMIN
# ========================================

@admin.register(ServiceRequest)
class ServiceRequestAdmin(admin.ModelAdmin):
    list_display = [
        'request_id', 'student', 'request_type', 'status', 
        'priority', 'assigned_staff', 'submitted_at'
    ]
    list_filter = ['status', 'request_type', 'priority', 'is_anonymous']
    search_fields = [
        'request_id', 'student__full_name', 'student__email',
        'subject', 'description'
    ]
    date_hierarchy = 'submitted_at'
    ordering = ['-submitted_at']
    
    fieldsets = (
        ('Request Info', {
            'fields': ('request_id', 'student', 'request_type', 'subject', 'description')
        }),
        ('Status & Assignment', {
            'fields': ('status', 'priority', 'assigned_staff', 'department')
        }),
        ('Response', {
            'fields': ('suggestion', 'resolution_notes', 'rejection_reason')
        }),
        ('Contact Info', {
            'fields': ('is_anonymous', 'student_name', 'admission_number', 'email', 'phone_number')
        }),
        ('Attachments', {
            'fields': ('attachment',)
        }),
        ('Timestamps', {
            'fields': ('submitted_at', 'resolved_at')
        }),
    )
    
    readonly_fields = ['request_id', 'submitted_at']


# ========================================
# ANNOUNCEMENT ADMIN
# ========================================

@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = [
        'announcement_id', 'title', 'posted_by', 'target_audience',
        'category', 'is_active', 'posted_at', 'expiry_date'
    ]
    list_filter = ['target_audience', 'is_active', 'category']
    search_fields = ['title', 'content', 'posted_by__full_name']
    date_hierarchy = 'posted_at'
    ordering = ['-posted_at']


# ========================================
# NOTIFICATION ADMIN
# ========================================

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = [
        'notification_id', 'user', 'title', 'notification_type',
        'channel', 'is_read', 'sent_at'
    ]
    list_filter = ['notification_type', 'channel', 'is_read']
    search_fields = ['user__full_name', 'user__email', 'title', 'message']
    date_hierarchy = 'sent_at'
    ordering = ['-sent_at']


# ========================================
# FEEDBACK ADMIN
# ========================================

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = [
        'feedback_id', 'submitted_by', 'department', 'rating',
        'is_reviewed', 'submitted_at'
    ]
    list_filter = ['rating', 'is_reviewed', 'department']
    search_fields = ['submitted_by__full_name', 'department', 'feedback_text']
    date_hierarchy = 'submitted_at'
    ordering = ['-submitted_at']


# ========================================
# ACADEMIC RESOURCE ADMIN
# ========================================

@admin.register(AcademicResource)
class AcademicResourceAdmin(admin.ModelAdmin):
    list_display = [
        'resource_id', 'title', 'category', 'uploaded_by',
        'is_public', 'download_count', 'uploaded_at'
    ]
    list_filter = ['category', 'is_public']
    search_fields = ['title', 'category', 'uploaded_by__full_name']
    date_hierarchy = 'uploaded_at'
    ordering = ['-uploaded_at']


# ========================================
# AUDIT LOG ADMIN
# ========================================

@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = [
        'log_id', 'user', 'action', 'table_affected',
        'ip_address', 'timestamp'
    ]
    list_filter = ['table_affected', 'timestamp']
    search_fields = ['user__full_name', 'action', 'details']
    date_hierarchy = 'timestamp'
    ordering = ['-timestamp']
    
    readonly_fields = ['log_id', 'user', 'action', 'table_affected', 
                       'timestamp', 'ip_address', 'user_agent', 'details']
    
    def has_add_permission(self, request):
        """Audit logs should not be manually added"""
        return False
    
    def has_delete_permission(self, request, obj=None):
        """Audit logs should not be deleted"""
        return False