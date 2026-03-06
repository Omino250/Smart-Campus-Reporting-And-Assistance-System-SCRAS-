# grievances/models.py

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator

# ========================================
# CUSTOM USER MODEL (Replaces default User)
# ========================================

class User(AbstractUser):
    """
    Extended User model with role-based access
    Replaces Django's default User model
    """
    ROLE_CHOICES = [
        ('student', 'Student'),
        ('staff', 'Staff'),
        ('admin', 'Administrator'),
    ]
    
    full_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='student')
    phone = models.CharField(max_length=20, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    
    # Student-specific fields
    student_id = models.CharField(max_length=50, blank=True, null=True, unique=True)
    admission_number = models.CharField(max_length=50, blank=True, null=True)
    year_of_study = models.IntegerField(blank=True, null=True)
    
    # Staff-specific fields
    staff_id = models.CharField(max_length=50, blank=True, null=True, unique=True)
    designation = models.CharField(max_length=100, blank=True, null=True)
    
    # Notification preferences
    email_notifications = models.BooleanField(default=True)
    in_app_notifications = models.BooleanField(default=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'full_name']
    
    def __str__(self):
        return f"{self.full_name} ({self.role})"
    
    class Meta:
        db_table = 'users'
        verbose_name = 'User'
        verbose_name_plural = 'Users'


# ========================================
# DEPARTMENT MODEL
# ========================================

class Department(models.Model):
    """University departments for request routing"""
    dept_code = models.CharField(max_length=10, unique=True, primary_key=True)
    dept_name = models.CharField(max_length=100)
    head_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.dept_code} - {self.dept_name}"
    
    class Meta:
        db_table = 'departments'
        ordering = ['dept_name']


# ========================================
# SERVICE REQUEST MODEL (Enhanced Grievance)
# ========================================

class ServiceRequest(models.Model):
    """
    Service/Grievance requests from students
    Enhanced version of your current Grievance model
    """
    REQUEST_TYPE_CHOICES = [
        ('maintenance', 'Maintenance'),
        ('academic', 'Academic'),
        ('administrative', 'Administrative'),
        ('it', 'IT Support'),
        ('harassment', 'Harassment'),
        ('financial', 'Financial'),
        ('mental', 'Mental Health'),
        ('other', 'Other'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
        ('rejected', 'Rejected'),
    ]
    
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]
    
    request_id = models.AutoField(primary_key=True)
    student = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='service_requests',
        limit_choices_to={'role': 'student'}
    )
    assigned_staff = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='assigned_requests',
        limit_choices_to={'role': 'staff'}
    )
    department = models.ForeignKey(
        Department,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    
    request_type = models.CharField(max_length=50, choices=REQUEST_TYPE_CHOICES)
    subject = models.CharField(max_length=200)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='medium')
    
    # Suggestion/Response
    suggestion = models.TextField(blank=True)
    resolution_notes = models.TextField(blank=True)
    rejection_reason = models.TextField(blank=True)
    
    # Contact info (for non-anonymous)
    is_anonymous = models.BooleanField(default=False)
    student_name = models.CharField(max_length=200, blank=True, null=True)
    admission_number = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    
    # Timestamps
    submitted_at = models.DateTimeField(default=timezone.now)
    resolved_at = models.DateTimeField(null=True, blank=True)
    
    # File attachment
    attachment = models.FileField(upload_to='request_attachments/', null=True, blank=True)
    
    class Meta:
        db_table = 'service_requests'
        ordering = ['-submitted_at']
        verbose_name = 'Service Request'
        verbose_name_plural = 'Service Requests'
    
    def __str__(self):
        return f"#{self.request_id} - {self.request_type} by {self.student.full_name}"


# ========================================
# ANNOUNCEMENT MODEL
# ========================================

class Announcement(models.Model):
    """Campus announcements posted by staff/admin"""
    TARGET_AUDIENCE_CHOICES = [
        ('all', 'All Users'),
        ('students', 'Students Only'),
        ('staff', 'Staff Only'),
    ]
    
    announcement_id = models.AutoField(primary_key=True)
    posted_by = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        limit_choices_to={'role__in': ['staff', 'admin']}
    )
    title = models.CharField(max_length=200)
    content = models.TextField()
    target_audience = models.CharField(
        max_length=20, 
        choices=TARGET_AUDIENCE_CHOICES, 
        default='all'
    )
    category = models.CharField(max_length=50, blank=True)
    posted_at = models.DateTimeField(auto_now_add=True)
    expiry_date = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'announcements'
        ordering = ['-posted_at']
    
    def __str__(self):
        return f"{self.title} - {self.posted_at.strftime('%Y-%m-%d')}"


# ========================================
# NOTIFICATION MODEL
# ========================================

class Notification(models.Model):
    """In-app and email notifications"""
    CHANNEL_CHOICES = [
        ('email', 'Email'),
        ('in_app', 'In-App'),
    ]
    
    notification_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    title = models.CharField(max_length=200)
    message = models.TextField()
    notification_type = models.CharField(max_length=50)  # request_update, announcement, etc.
    channel = models.CharField(max_length=20, choices=CHANNEL_CHOICES, default='in_app')
    is_read = models.BooleanField(default=False)
    sent_at = models.DateTimeField(auto_now_add=True)
    
    # Optional link to related object
    related_request = models.ForeignKey(
        ServiceRequest, 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True
    )
    
    class Meta:
        db_table = 'notifications'
        ordering = ['-sent_at']
    
    def __str__(self):
        return f"{self.title} - {self.user.full_name}"


# ========================================
# FEEDBACK MODEL
# ========================================

class Feedback(models.Model):
    """User feedback on services and requests"""
    feedback_id = models.AutoField(primary_key=True)
    submitted_by = models.ForeignKey(User, on_delete=models.CASCADE)
    department = models.CharField(max_length=100)
    feedback_text = models.TextField()
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    submitted_at = models.DateTimeField(auto_now_add=True)
    is_reviewed = models.BooleanField(default=False)
    
    # Optional: Link to specific request
    related_request = models.ForeignKey(
        ServiceRequest,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    
    class Meta:
        db_table = 'feedback'
        ordering = ['-submitted_at']
    
    def __str__(self):
        return f"Feedback by {self.submitted_by.full_name} - {self.rating}★"


# ========================================
# ACADEMIC RESOURCE MODEL
# ========================================

class AcademicResource(models.Model):
    """Academic materials and resources"""
    resource_id = models.AutoField(primary_key=True)
    uploaded_by = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'staff'}
    )
    title = models.CharField(max_length=200)
    category = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    file = models.FileField(upload_to='academic_resources/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    is_public = models.BooleanField(default=True)
    download_count = models.IntegerField(default=0)
    
    class Meta:
        db_table = 'academic_resources'
        ordering = ['-uploaded_at']
    
    def __str__(self):
        return self.title


# ========================================
# AUDIT LOG MODEL
# ========================================

class AuditLog(models.Model):
    """System audit trail for security and monitoring"""
    log_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    action = models.CharField(max_length=200)
    table_affected = models.CharField(max_length=50, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.CharField(max_length=300, blank=True)
    details = models.TextField(blank=True)
    
    class Meta:
        db_table = 'audit_log'
        ordering = ['-timestamp']
    
    def __str__(self):
        return f"{self.action} by {self.user} at {self.timestamp}"