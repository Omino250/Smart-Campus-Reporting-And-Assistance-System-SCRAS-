# grievances/audit.py

from .models import AuditLog

class AuditLogger:
    """
    Utility for logging user actions for security and monitoring
    Based on ERD specifications
    """
    
    @staticmethod
    def log_action(user, action, table_affected='', request=None, details=''):
        """Log a user action to audit trail"""
        try:
            ip_address = None
            user_agent = ''
            
            if request:
                # Get IP address
                x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
                if x_forwarded_for:
                    ip_address = x_forwarded_for.split(',')[0]
                else:
                    ip_address = request.META.get('REMOTE_ADDR')
                
                # Get user agent
                user_agent = request.META.get('HTTP_USER_AGENT', '')[:300]
            
            AuditLog.objects.create(
                user=user,
                action=action,
                table_affected=table_affected,
                ip_address=ip_address,
                user_agent=user_agent,
                details=details
            )
        except Exception as e:
            print(f"Error logging audit action: {e}")
    
    @staticmethod
    def log_login(user, request):
        """Log user login"""
        AuditLogger.log_action(
            user, 
            f"User logged in: {user.email}", 
            'users', 
            request
        )
    
    @staticmethod
    def log_logout(user, request):
        """Log user logout"""
        AuditLogger.log_action(
            user, 
            f"User logged out: {user.email}", 
            'users', 
            request
        )
    
    @staticmethod
    def log_request_submission(user, service_request, request):
        """Log service request submission"""
        AuditLogger.log_action(
            user,
            f"Submitted service request #{service_request.request_id}",
            'service_requests',
            request,
            f"Type: {service_request.request_type}, Priority: {service_request.priority}"
        )
    
    @staticmethod
    def log_request_status_change(user, service_request, old_status, new_status, request):
        """Log request status change"""
        AuditLogger.log_action(
            user,
            f"Changed status of request #{service_request.request_id}",
            'service_requests',
            request,
            f"From: {old_status} → To: {new_status}"
        )