# grievances/notifications.py

from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from .models import Notification, User

class NotificationService:
    """
    Handles all notification logic (email + in-app)
    Based on DFD Level 4 specifications
    """
    
    @staticmethod
    def send_notification(user, title, message, notification_type, related_request=None):
        """
        Main notification dispatcher
        Checks user preferences and sends via appropriate channels
        """
        # Check user preferences
        if user.in_app_notifications:
            NotificationService._create_in_app_notification(
                user, title, message, notification_type, related_request
            )
        
        if user.email_notifications and user.email:
            NotificationService._send_email_notification(
                user, title, message, notification_type
            )
    
    @staticmethod
    def _create_in_app_notification(user, title, message, notification_type, related_request):
        """Store in-app notification in database"""
        try:
            Notification.objects.create(
                user=user,
                title=title,
                message=message,
                notification_type=notification_type,
                channel='in_app',
                related_request=related_request
            )
        except Exception as e:
            print(f"Error creating in-app notification: {e}")
    
    @staticmethod
    def _send_email_notification(user, title, message, notification_type):
        """Send email notification via SMTP"""
        try:
            subject = f"SCRAS: {title}"
            
            # HTML email template
            html_message = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <style>
                    body {{ font-family: Arial, sans-serif; line-height: 1.6; }}
                    .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                    .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                              color: white; padding: 20px; text-align: center; }}
                    .content {{ padding: 20px; background: #f8f9fa; }}
                    .footer {{ text-align: center; padding: 20px; color: #666; font-size: 12px; }}
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        <h2>🎓 SCRAS Notification</h2>
                    </div>
                    <div class="content">
                        <h3>{title}</h3>
                        <p>{message}</p>
                        <p><a href="http://127.0.0.1:8000/" style="background: #667eea; color: white; 
                           padding: 10px 20px; text-decoration: none; border-radius: 5px;">
                           View in SCRAS</a></p>
                    </div>
                    <div class="footer">
                        <p>Smart Campus Reporting and Assistance System<br>
                        Maseno University | This is an automated message</p>
                    </div>
                </div>
            </body>
            </html>
            """
            
            send_mail(
                subject=subject,
                message=message,  # Plain text fallback
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                html_message=html_message,
                fail_silently=True  # Don't crash if email fails
            )
            
            # Log email notification
            Notification.objects.create(
                user=user,
                title=title,
                message=message,
                notification_type=notification_type,
                channel='email'
            )
        except Exception as e:
            print(f"Error sending email notification: {e}")
    
    @staticmethod
    def notify_request_submitted(service_request):
        """Notification when request is submitted"""
        user = service_request.student
        title = f"Request #{service_request.request_id} Submitted"
        message = f"Your {service_request.request_type} request has been received and is being reviewed."
        
        NotificationService.send_notification(
            user, title, message, 'request_submitted', service_request
        )
    
    @staticmethod
    def notify_request_status_changed(service_request):
        """Notification when request status changes"""
        user = service_request.student
        title = f"Request #{service_request.request_id} Status Updated"
        message = f"Your request status has been changed to: {service_request.get_status_display()}"
        
        NotificationService.send_notification(
            user, title, message, 'request_status_update', service_request
        )
    
    @staticmethod
    def notify_request_assigned(service_request, staff):
        """Notification to staff when request is assigned"""
        title = f"New Request Assigned: #{service_request.request_id}"
        message = f"A new {service_request.request_type} request has been assigned to you."
        
        NotificationService.send_notification(
            staff, title, message, 'request_assigned', service_request
        )
    
    @staticmethod
    def notify_new_announcement(announcement, target_users):
        """Notification for new announcements"""
        title = f"New Announcement: {announcement.title}"
        message = announcement.content[:200] + "..."
        
        for user in target_users:
            NotificationService.send_notification(
                user, title, message, 'announcement'
            )