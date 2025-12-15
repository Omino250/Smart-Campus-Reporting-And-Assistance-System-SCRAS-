# scras/urls.py (Main project URLs)

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('grievances.urls')),
]