# grievances/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import (
    User, ServiceRequest, Announcement, 
    Feedback, AcademicResource, Department
)

# ========================================
# USER REGISTRATION FORM
# ========================================

class StudentRegistrationForm(UserCreationForm):
    """Registration form for new students"""
    full_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Full Name'
        })
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'university.email@maseno.ac.ke'
        })
    )
    student_id = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Student ID'
        })
    )
    admission_number = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'e.g., TMC/00025/024'
        })
    )
    phone = forms.CharField(
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '+254 700 000 000'
        })
    )
    year_of_study = forms.IntegerField(
        min_value=1,
        max_value=6,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Year (1-6)'
        })
    )
    
    class Meta:
        model = User
        fields = ['full_name', 'email', 'username', 'student_id', 
                  'admission_number', 'phone', 'year_of_study', 
                  'password1', 'password2']
        
    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'student'
        if commit:
            user.save()
        return user


# ========================================
# SERVICE REQUEST FORM (Enhanced)
# ========================================

class ServiceRequestForm(forms.ModelForm):
    """Form for submitting service requests"""
    
    class Meta:
        model = ServiceRequest
        fields = [
            'request_type',
            'subject', 
            'description',
            'priority',
            'is_anonymous',
            'student_name',
            'admission_number',
            'email',
            'phone_number',
            'attachment'
        ]
        widgets = {
            'request_type': forms.Select(attrs={
                'class': 'form-select',
                'required': True
            }),
            'subject': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Brief subject/title',
                'maxlength': '200'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 6,
                'placeholder': 'Please describe your issue in detail...',
                'required': True
            }),
            'priority': forms.Select(attrs={
                'class': 'form-select'
            }),
            'is_anonymous': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
                'id': 'anonymousCheck'
            }),
            'student_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your full name',
                'id': 'studentName'
            }),
            'admission_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., TMC/00025/024',
                'id': 'admissionNumber'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'your.email@university.edu',
                'id': 'studentEmail'
            }),
            'phone_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+254 700 000 000',
                'id': 'phoneNumber'
            }),
            'attachment': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': '.pdf,.jpg,.jpeg,.png,.doc,.docx'
            })
        }
        labels = {
            'request_type': 'Request Type',
            'subject': 'Subject',
            'description': 'Describe Your Issue',
            'priority': 'Priority Level',
            'is_anonymous': 'Submit Anonymously',
            'student_name': 'Full Name',
            'admission_number': 'Admission Number',
            'email': 'Email Address',
            'phone_number': 'Phone Number',
            'attachment': 'Attach File (Optional)'
        }
        help_texts = {
            'is_anonymous': 'Check this box if you prefer to remain anonymous',
            'description': 'Provide as much detail as possible',
            'attachment': 'Max file size: 5MB. Supported: PDF, Images, Word docs'
        }


# ========================================
# REQUEST STATUS UPDATE FORM (Staff)
# ========================================

class RequestStatusUpdateForm(forms.ModelForm):
    """Form for staff to update request status"""
    
    class Meta:
        model = ServiceRequest
        fields = ['status', 'resolution_notes', 'rejection_reason']
        widgets = {
            'status': forms.Select(attrs={
                'class': 'form-select'
            }),
            'resolution_notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Enter resolution details...'
            }),
            'rejection_reason': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Reason for rejection (if applicable)'
            })
        }


# ========================================
# ANNOUNCEMENT FORM
# ========================================

class AnnouncementForm(forms.ModelForm):
    """Form for posting announcements"""
    
    class Meta:
        model = Announcement
        fields = ['title', 'content', 'target_audience', 'category', 'expiry_date']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Announcement Title'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 8,
                'placeholder': 'Announcement content...'
            }),
            'target_audience': forms.Select(attrs={
                'class': 'form-select'
            }),
            'category': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Academic, Events, Urgent'
            }),
            'expiry_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            })
        }


# ========================================
# FEEDBACK FORM
# ========================================

class FeedbackForm(forms.ModelForm):
    """Form for submitting feedback"""
    
    class Meta:
        model = Feedback
        fields = ['department', 'rating', 'feedback_text', 'related_request']
        widgets = {
            'department': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Department name'
            }),
            'rating': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1',
                'max': '5',
                'placeholder': 'Rate 1-5'
            }),
            'feedback_text': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Your feedback...'
            }),
            'related_request': forms.Select(attrs={
                'class': 'form-select'
            })
        }
        labels = {
            'department': 'Department',
            'rating': 'Rating (1-5 stars)',
            'feedback_text': 'Your Feedback',
            'related_request': 'Related Request (Optional)'
        }


# ========================================
# ACADEMIC RESOURCE FORM
# ========================================

class AcademicResourceForm(forms.ModelForm):
    """Form for uploading academic resources"""
    
    class Meta:
        model = AcademicResource
        fields = ['title', 'category', 'description', 'file', 'is_public']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Resource Title'
            }),
            'category': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Lecture Notes, Past Papers'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Description of the resource...'
            }),
            'file': forms.FileInput(attrs={
                'class': 'form-control'
            }),
            'is_public': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            })
        }


# ========================================
# DEPARTMENT FORM
# ========================================

class DepartmentForm(forms.ModelForm):
    """Form for managing departments"""
    
    class Meta:
        model = Department
        fields = ['dept_code', 'dept_name', 'head_name', 'email', 'phone']
        widgets = {
            'dept_code': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., CS, MATH'
            }),
            'dept_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Department Name'
            }),
            'head_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Head of Department'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'department@maseno.ac.ke'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+254 700 000 000'
            })
        }


# ========================================
# USER PROFILE UPDATE FORM
# ========================================

class ProfileUpdateForm(forms.ModelForm):
    """Form for users to update their profile"""
    
    class Meta:
        model = User
        fields = ['full_name', 'phone', 'email_notifications', 'in_app_notifications']
        widgets = {
            'full_name': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'email_notifications': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'in_app_notifications': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            })
        }