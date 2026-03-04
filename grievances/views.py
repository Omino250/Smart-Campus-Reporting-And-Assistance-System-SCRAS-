# grievances/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views import View
from django.utils import timezone
from django.db.models import Q, Count
from django.http import JsonResponse, HttpResponseForbidden

from .models import (
    User, ServiceRequest, Announcement, Notification, 
    Feedback, AcademicResource, Department
)
from .forms import (
    ServiceRequestForm, AnnouncementForm, FeedbackForm,
    RequestStatusUpdateForm, StudentRegistrationForm,
    AcademicResourceForm, ProfileUpdateForm
)
from .suggestion_engine import generate_suggestion
from .notifications import NotificationService
from .audit import AuditLogger


# ========================================
# HOME & AUTHENTICATION VIEWS
# ========================================

def home(request):
    """Landing page - redirect based on auth status"""
    if request.user.is_authenticated:
        # Redirect to role-based dashboard
        if request.user.role == 'student':
            return redirect('grievances:student_dashboard')
        elif request.user.role == 'staff':
            return redirect('grievances:staff_dashboard')
        elif request.user.role == 'admin':
            return redirect('grievances:admin_dashboard')
    
    return render(request, 'grievances/index.html')


def user_register(request):
    """Student registration"""
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Registration successful! Please login.')
            return redirect('grievances:user_login')
    else:
        form = StudentRegistrationForm()
    
    return render(request, 'grievances/register.html', {'form': form})


def user_login(request):
    """User login"""
    if request.user.is_authenticated:
        return redirect('grievances:home')
    
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        # Authenticate by email
        user = authenticate(request, username=email, password=password)
        
        if user is not None:
            login(request, user)
            
            # Log the login
            AuditLogger.log_login(user, request)
            
            # Redirect based on role
            if user.role == 'student':
                return redirect('grievances:student_dashboard')
            elif user.role == 'staff':
                return redirect('grievances:staff_dashboard')
            elif user.role == 'admin':
                return redirect('grievances:admin_dashboard')
        else:
            messages.error(request, 'Invalid email or password.')
    
    return render(request, 'grievances/login.html')


@login_required
def user_logout(request):
    """User logout"""
    AuditLogger.log_logout(request.user, request)
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('grievances:home')


# ========================================
# STUDENT DASHBOARD
# ========================================

@login_required
def student_dashboard(request):
    """Student dashboard"""
    if request.user.role != 'student':
        return HttpResponseForbidden("Access denied")
    
    # Get statistics
    my_requests = ServiceRequest.objects.filter(student=request.user)
    pending_count = my_requests.filter(status='pending').count()
    resolved_count = my_requests.filter(status='resolved').count()
    
    # Get recent announcements
    recent_announcements = Announcement.objects.filter(
        Q(target_audience='all') | Q(target_audience='students'),
        is_active=True
    ).order_by('-posted_at')[:3]
    
    # Get unread notifications
    unread_notifications = Notification.objects.filter(
        user=request.user,
        is_read=False
    ).count()
    
    context = {
        'my_requests_count': my_requests.count(),
        'pending_count': pending_count,
        'resolved_count': resolved_count,
        'recent_announcements': recent_announcements,
        'unread_notifications': unread_notifications,
    }
    
    return render(request, 'grievances/student_dashboard.html', context)


# ========================================
# SERVICE REQUEST VIEWS
# ========================================

@login_required
def submit_request(request):
    """Submit new service request"""
    if request.user.role != 'student':
        return HttpResponseForbidden("Only students can submit requests")
    
    if request.method == 'POST':
        form = ServiceRequestForm(request.POST, request.FILES)
        if form.is_valid():
            service_request = form.save(commit=False)
            service_request.student = request.user
            
            # Validate contact info for non-anonymous
            if not service_request.is_anonymous:
                if not all([service_request.student_name, service_request.admission_number,
                           service_request.email, service_request.phone_number]):
                    form.add_error(None, 'Please provide all contact information for non-anonymous submissions.')
                    return render(request, 'grievances/submit_request.html', {'form': form})
            
            # Clear contact info if anonymous
            if service_request.is_anonymous:
                service_request.student_name = None
                service_request.admission_number = None
                service_request.email = None
                service_request.phone_number = None
            
            # Generate suggestion
            suggestion = generate_suggestion(
                service_request.request_type,
                service_request.description
            )
            service_request.suggestion = suggestion
            
            # Auto-assign to department (simple logic - can be enhanced)
            # For now, we'll leave it unassigned
            
            service_request.save()
            
            # Log the action
            AuditLogger.log_request_submission(request.user, service_request, request)
            
            # Send notification
            NotificationService.notify_request_submitted(service_request)
            
            messages.success(request, f'Request #{service_request.request_id} submitted successfully!')
            return redirect('grievances:request_detail', pk=service_request.request_id)
    else:
        form = ServiceRequestForm()
    
    return render(request, 'grievances/submit_request.html', {'form': form})


@login_required
def my_requests(request):
    """View all requests by current student"""
    if request.user.role != 'student':
        return HttpResponseForbidden("Access denied")
    
    # Filter by status if provided
    status_filter = request.GET.get('status', 'all')
    
    requests = ServiceRequest.objects.filter(student=request.user)
    
    if status_filter != 'all':
        requests = requests.filter(status=status_filter)
    
    context = {
        'requests': requests,
        'status_filter': status_filter,
        'total_count': requests.count(),
    }
    
    return render(request, 'grievances/my_requests.html', context)


@login_required
def request_detail(request, pk):
    """View detailed information about a request"""
    service_request = get_object_or_404(ServiceRequest, request_id=pk)
    
    # Check permissions
    if request.user.role == 'student':
        if service_request.student != request.user:
            return HttpResponseForbidden("You can only view your own requests")
    elif request.user.role not in ['staff', 'admin']:
        return HttpResponseForbidden("Access denied")
    
    context = {
        'request': service_request,
    }
    
    return render(request, 'grievances/request_detail.html', context)


# ========================================
# STAFF VIEWS
# ========================================

@login_required
def staff_dashboard(request):
    """Staff dashboard"""
    if request.user.role != 'staff':
        return HttpResponseForbidden("Access denied")
    
    # Get assigned requests
    assigned_requests = ServiceRequest.objects.filter(assigned_staff=request.user)
    pending_requests = assigned_requests.filter(status='pending')
    in_progress_requests = assigned_requests.filter(status='in_progress')
    
    # Get all pending requests for assignment
    unassigned_requests = ServiceRequest.objects.filter(
        assigned_staff__isnull=True,
        status='pending'
    )
    
    context = {
        'pending_count': pending_requests.count(),
        'in_progress_count': in_progress_requests.count(),
        'total_assigned': assigned_requests.count(),
        'pending_requests': pending_requests[:5],
        'unassigned_requests': unassigned_requests[:5],
    }
    
    return render(request, 'grievances/staff_dashboard.html', context)


@login_required
def staff_requests_list(request):
    """View all requests for staff"""
    if request.user.role not in ['staff', 'admin']:
        return HttpResponseForbidden("Access denied")
    
    # Filter options
    status_filter = request.GET.get('status', 'all')
    assignment_filter = request.GET.get('assignment', 'all')
    
    if request.user.role == 'staff':
        requests = ServiceRequest.objects.filter(assigned_staff=request.user)
    else:  # admin
        requests = ServiceRequest.objects.all()
    
    if status_filter != 'all':
        requests = requests.filter(status=status_filter)
    
    if assignment_filter == 'unassigned':
        requests = requests.filter(assigned_staff__isnull=True)
    elif assignment_filter == 'assigned':
        requests = requests.filter(assigned_staff__isnull=False)
    
    context = {
        'requests': requests,
        'status_filter': status_filter,
        'assignment_filter': assignment_filter,
    }
    
    return render(request, 'grievances/staff_requests_list.html', context)


@login_required
def update_request_status(request, pk):
    """Staff updates request status"""
    if request.user.role not in ['staff', 'admin']:
        return HttpResponseForbidden("Access denied")
    
    service_request = get_object_or_404(ServiceRequest, request_id=pk)
    
    # Store old status for logging
    old_status = service_request.status
    
    if request.method == 'POST':
        form = RequestStatusUpdateForm(request.POST, instance=service_request)
        if form.is_valid():
            service_request = form.save(commit=False)
            
            # If resolved, set resolved_at timestamp
            if service_request.status == 'resolved' and old_status != 'resolved':
                service_request.resolved_at = timezone.now()
            
            service_request.save()
            
            # Log the action
            AuditLogger.log_request_status_change(
                request.user, service_request, old_status, 
                service_request.status, request
            )
            
            # Send notification to student
            NotificationService.notify_request_status_changed(service_request)
            
            messages.success(request, 'Request status updated successfully!')
            return redirect('grievances:request_detail', pk=pk)
    else:
        form = RequestStatusUpdateForm(instance=service_request)
    
    context = {
        'form': form,
        'request': service_request,
    }
    
    return render(request, 'grievances/update_request_status.html', context)


@login_required
def assign_request_to_self(request, pk):
    """Staff assigns a request to themselves"""
    if request.user.role != 'staff':
        return HttpResponseForbidden("Access denied")
    
    service_request = get_object_or_404(ServiceRequest, request_id=pk)
    service_request.assigned_staff = request.user
    service_request.save()
    
    # Notify staff
    NotificationService.notify_request_assigned(service_request, request.user)
    
    messages.success(request, f'Request #{pk} assigned to you!')
    return redirect('grievances:request_detail', pk=pk)


# ========================================
# ANNOUNCEMENT VIEWS
# ========================================

@login_required
def announcements_list(request):
    """View all announcements"""
    # Filter by target audience
    if request.user.role == 'student':
        announcements = Announcement.objects.filter(
            Q(target_audience='all') | Q(target_audience='students'),
            is_active=True
        )
    elif request.user.role == 'staff':
        announcements = Announcement.objects.filter(
            Q(target_audience='all') | Q(target_audience='staff'),
            is_active=True
        )
    else:  # admin
        announcements = Announcement.objects.filter(is_active=True)
    
    # Search functionality
    search_query = request.GET.get('q', '')
    if search_query:
        announcements = announcements.filter(
            Q(title__icontains=search_query) | Q(content__icontains=search_query)
        )
    
    context = {
        'announcements': announcements,
        'search_query': search_query,
    }
    
    return render(request, 'grievances/announcements_list.html', context)


@login_required
def announcement_detail(request, pk):
    """View announcement details"""
    announcement = get_object_or_404(Announcement, announcement_id=pk)
    
    return render(request, 'grievances/announcement_detail.html', {
        'announcement': announcement
    })


@login_required
def create_announcement(request):
    """Create new announcement (staff/admin only)"""
    if request.user.role not in ['staff', 'admin']:
        return HttpResponseForbidden("Only staff and admins can post announcements")
    
    if request.method == 'POST':
        form = AnnouncementForm(request.POST)
        if form.is_valid():
            announcement = form.save(commit=False)
            announcement.posted_by = request.user
            announcement.save()
            
            # Notify target users
            if announcement.target_audience == 'all':
                target_users = User.objects.filter(is_active=True)
            elif announcement.target_audience == 'students':
                target_users = User.objects.filter(role='student', is_active=True)
            else:  # staff
                target_users = User.objects.filter(role='staff', is_active=True)
            
            NotificationService.notify_new_announcement(announcement, target_users)
            
            messages.success(request, 'Announcement posted successfully!')
            return redirect('grievances:announcements_list')
    else:
        form = AnnouncementForm()
    
    return render(request, 'grievances/create_announcement.html', {'form': form})


# ========================================
# NOTIFICATION VIEWS
# ========================================

@login_required
def notifications_list(request):
    """View all notifications"""
    notifications = Notification.objects.filter(user=request.user)
    
    # Mark as read when viewed
    unread = notifications.filter(is_read=False)
    
    context = {
        'notifications': notifications,
        'unread_count': unread.count(),
    }
    
    return render(request, 'grievances/notifications_list.html', context)


@login_required
def mark_notification_read(request, pk):
    """Mark notification as read"""
    notification = get_object_or_404(Notification, notification_id=pk, user=request.user)
    notification.is_read = True
    notification.save()
    
    return redirect('grievances:notifications_list')


@login_required
def mark_all_notifications_read(request):
    """Mark all notifications as read"""
    Notification.objects.filter(user=request.user, is_read=False).update(is_read=True)
    messages.success(request, 'All notifications marked as read')
    return redirect('grievances:notifications_list')


# ========================================
# FEEDBACK VIEWS
# ========================================

@login_required
def submit_feedback(request):
    """Submit feedback"""
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.submitted_by = request.user
            feedback.save()
            
            messages.success(request, 'Thank you for your feedback!')
            return redirect('grievances:student_dashboard')
    else:
        # Pre-fill related request if provided
        request_id = request.GET.get('request_id')
        if request_id:
            form = FeedbackForm(initial={'related_request': request_id})
        else:
            form = FeedbackForm()
    
    return render(request, 'grievances/submit_feedback.html', {'form': form})


# ========================================
# ADMIN VIEWS
# ========================================

@login_required
def admin_dashboard(request):
    """Admin dashboard with statistics"""
    if request.user.role != 'admin':
        return HttpResponseForbidden("Access denied - Admin only")
    
    # Get comprehensive statistics
    total_users = User.objects.count()
    total_students = User.objects.filter(role='student').count()
    total_staff = User.objects.filter(role='staff').count()
    
    total_requests = ServiceRequest.objects.count()
    pending_requests = ServiceRequest.objects.filter(status='pending').count()
    resolved_requests = ServiceRequest.objects.filter(status='resolved').count()
    
    total_announcements = Announcement.objects.filter(is_active=True).count()
    total_feedback = Feedback.objects.count()
    
    # Recent activity
    recent_requests = ServiceRequest.objects.all()[:5]
    recent_users = User.objects.order_by('-date_joined')[:5]
    
    context = {
        'total_users': total_users,
        'total_students': total_students,
        'total_staff': total_staff,
        'total_requests': total_requests,
        'pending_requests': pending_requests,
        'resolved_requests': resolved_requests,
        'total_announcements': total_announcements,
        'total_feedback': total_feedback,
        'recent_requests': recent_requests,
        'recent_users': recent_users,
    }
    
    return render(request, 'grievances/admin_dashboard.html', context)


@login_required
def view_audit_logs(request):
    """View system audit logs"""
    if request.user.role != 'admin':
        return HttpResponseForbidden("Access denied - Admin only")
    
    from .models import AuditLog
    
    logs = AuditLog.objects.all()[:100]  # Last 100 logs
    
    return render(request, 'grievances/audit_logs.html', {'logs': logs})


# ========================================
# PROFILE MANAGEMENT
# ========================================

@login_required
def user_profile(request):
    """View and edit user profile"""
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('grievances:user_profile')
    else:
        form = ProfileUpdateForm(instance=request.user)
    
    context = {
        'form': form,
        'user': request.user,
    }
    
    return render(request, 'grievances/profile.html', context)


# ========================================
# API ENDPOINTS (For AJAX/JSON responses)
# ========================================

@login_required
def get_unread_notifications_count(request):
    """API endpoint for notification badge count"""
    count = Notification.objects.filter(user=request.user, is_read=False).count()
    return JsonResponse({'count': count})