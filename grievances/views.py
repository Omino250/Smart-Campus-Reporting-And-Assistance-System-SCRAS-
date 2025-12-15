# grievances/views.py

from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Grievance
from .forms import GrievanceForm
from .suggestion_engine import generate_suggestion

def home(request):
    """Home page - only show Submit Issue button"""
    return render(request, 'grievances/index.html')

class SubmitGrievanceView(View):
    """Handle grievance submission"""
    
    def get(self, request):
        form = GrievanceForm()
        return render(request, 'grievances/report.html', {'form': form})
    
    def post(self, request):
        form = GrievanceForm(request.POST)
        if form.is_valid():
            grievance = form.save(commit=False)
            
            # Generate suggestion based on category and description
            suggestion = generate_suggestion(
                grievance.category,
                grievance.description
            )
            grievance.suggestion = suggestion
            grievance.save()
            
            # Pass the grievance to thank you page
            return render(request, 'grievances/thank_you.html', {
                'suggestion': suggestion,
                'category': grievance.get_category_display()
            })
        
        return render(request, 'grievances/report.html', {'form': form})

def admin_login(request):
    """Admin login page"""
    if request.user.is_authenticated:
        return redirect('grievances:admin_dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None and user.is_staff:
            login(request, user)
            return redirect('grievances:admin_dashboard')
        else:
            messages.error(request, 'Invalid credentials or unauthorized access.')
    
    return render(request, 'grievances/admin_login.html')

@login_required(login_url='grievances:admin_login')
def admin_dashboard(request):
    """Admin view to see all submissions - PROTECTED"""
    if not request.user.is_staff:
        messages.error(request, 'Unauthorized access.')
        return redirect('grievances:home')
    
    grievances = Grievance.objects.all()
    
    # Get statistics
    total_count = grievances.count()
    pending_count = grievances.filter(status='pending').count()
    anonymous_count = grievances.filter(is_anonymous=True).count()
    
    context = {
        'grievances': grievances,
        'total_count': total_count,
        'pending_count': pending_count,
        'anonymous_count': anonymous_count,
    }
    
    return render(request, 'grievances/admin_dashboard.html', context)

def admin_logout(request):
    """Logout admin"""
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('grievances:home')