# grievances/forms.py

from django import forms
from .models import Grievance

class GrievanceForm(forms.ModelForm):
    class Meta:
        model = Grievance
        fields = ['category', 'description', 'is_anonymous']
        widgets = {
            'category': forms.Select(attrs={
                'class': 'form-select',
                'required': True
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 6,
                'placeholder': 'Please describe your issue in detail...',
                'required': True
            }),
            'is_anonymous': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            })
        }
        labels = {
            'category': 'Issue Category',
            'description': 'Describe Your Issue',
            'is_anonymous': 'Submit Anonymously'
        }
        help_texts = {
            'is_anonymous': 'Check this box if you prefer to remain anonymous',
            'description': 'Provide as much detail as possible to help us assist you better'
        }