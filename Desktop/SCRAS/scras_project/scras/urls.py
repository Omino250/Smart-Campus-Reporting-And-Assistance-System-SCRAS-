# scras/urls.py

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('grievances.urls')),
     path('accounts/', include('django.contrib.auth.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    # scras/urls.py
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('grievances.urls', namespace='grievances')),

    # ========================================
    # PASSWORD RESET FLOW (4 steps)
    # ========================================
    path('password-reset/',
        auth_views.PasswordResetView.as_view(
            template_name='grievances/password_reset.html',
            email_template_name='grievances/password_reset_email.html',
            subject_template_name='grievances/password_reset_subject.txt',
            success_url='/password-reset/done/'
        ),
        name='password_reset'),

    path('password-reset/done/',
        auth_views.PasswordResetDoneView.as_view(
            template_name='grievances/password_reset_done.html'
        ),
        name='password_reset_done'),

    path('password-reset-confirm/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(
            template_name='grievances/password_reset_confirm.html',
            success_url='/password-reset/complete/'
        ),
        name='password_reset_confirm'),

    path('password-reset/complete/',
        auth_views.PasswordResetCompleteView.as_view(
            template_name='grievances/password_reset_complete.html'
        ),
        name='password_reset_complete'),
]