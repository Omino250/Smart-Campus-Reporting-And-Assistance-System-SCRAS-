# grievances/models.py

from django.db import models
from django.utils import timezone

class Grievance(models.Model):
    CATEGORY_CHOICES = [
        ('academic', 'Academic'),
        ('harassment', 'Harassment'),
        ('financial', 'Financial'),
        ('mental', 'Mental Health'),
        ('other', 'Other'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('reviewed', 'Reviewed'),
        ('resolved', 'Resolved'),
    ]
    
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    description = models.TextField()
    is_anonymous = models.BooleanField(default=False)
    suggestion = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    submitted_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        ordering = ['-submitted_at']
        verbose_name = 'Grievance'
        verbose_name_plural = 'Grievances'
    
    def __str__(self):
        return f"{self.category} - {self.submitted_at.strftime('%Y-%m-%d %H:%M')}"
