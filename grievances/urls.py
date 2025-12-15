# grievances/urls.py

# grievances/urls.py

from django.urls import path
from . import views

app_name = 'grievances'

urlpatterns = [
    path('', views.home, name='home'),
    path('report/', views.SubmitGrievanceView.as_view(), name='report'),
    path('admin-login/', views.admin_login, name='admin_login'),
    path('admin-panel/', views.admin_dashboard, name='admin_dashboard'),
    path('admin-logout/', views.admin_logout, name='admin_logout'),
]
