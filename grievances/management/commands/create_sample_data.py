# grievances/management/commands/create_sample_data.py

from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from grievances.models import User, Department, ServiceRequest, Announcement
import random

class Command(BaseCommand):
    help = 'Creates sample data for SCRAS system'

    def handle(self, *args, **kwargs):
        self.stdout.write('Creating sample data...')
        
        # Create departments
        departments_data = [
            {'dept_code': 'CS', 'dept_name': 'Computer Science', 'head_name': 'Dr. Jane Smith', 
             'email': 'cs@maseno.ac.ke', 'phone': '+254-057-351622'},
            {'dept_code': 'MATH', 'dept_name': 'Mathematics', 'head_name': 'Prof. John Doe',
             'email': 'math@maseno.ac.ke', 'phone': '+254-057-351623'},
            {'dept_code': 'ENG', 'dept_name': 'Engineering', 'head_name': 'Dr. Mary Johnson',
             'email': 'eng@maseno.ac.ke', 'phone': '+254-057-351624'},
        ]
        
        for dept_data in departments_data:
            Department.objects.get_or_create(**dept_data)
        
        self.stdout.write(self.style.SUCCESS('✓ Created departments'))
        
        # Create admin user
        admin, created = User.objects.get_or_create(
            email='admin@scras.maseno.ac.ke',
            defaults={
                'username': 'admin',
                'full_name': 'System Administrator',
                'role': 'admin',
                'is_staff': True,
                'is_superuser': True,
            }
        )
        if created:
            admin.set_password('admin123')
            admin.save()
            self.stdout.write(self.style.SUCCESS('✓ Created admin user'))
        
        # Create staff users
        staff_data = [
            {'email': 'staff1@maseno.ac.ke', 'full_name': 'Alice Wanjiru', 'staff_id': 'STF001'},
            {'email': 'staff2@maseno.ac.ke', 'full_name': 'Bob Ochieng', 'staff_id': 'STF002'},
        ]
        
        for staff_info in staff_data:
            staff, created = User.objects.get_or_create(
                email=staff_info['email'],
                defaults={
                    'username': staff_info['email'].split('@')[0],
                    'full_name': staff_info['full_name'],
                    'role': 'staff',
                    'staff_id': staff_info['staff_id'],
                    'is_staff': True,
                }
            )
            if created:
                staff.set_password('staff123')
                staff.save()
        
        self.stdout.write(self.style.SUCCESS('✓ Created staff users'))
        
        # Create student users
        for i in range(1, 6):
            student, created = User.objects.get_or_create(
                email=f'student{i}@students.maseno.ac.ke',
                defaults={
                    'username': f'student{i}',
                    'full_name': f'Student {i}',
                    'role': 'student',
                    'student_id': f'STD00{i}',
                    'admission_number': f'TMC/0000{i}/024',
                    'year_of_study': random.randint(1, 4),
                }
            )
            if created:
                student.set_password('student123')
                student.save()
        
        self.stdout.write(self.style.SUCCESS('✓ Created student users'))
        
        # Create sample announcements
        staff_user = User.objects.filter(role='staff').first()
        announcements_data = [
            {
                'title': 'Semester Registration Deadline',
                'content': 'All students are reminded that semester registration closes on Friday, March 15th.',
                'target_audience': 'students',
                'category': 'Academic',
            },
            {
                'title': 'Staff Meeting - March 10th',
                'content': 'All staff members are required to attend the departmental meeting on March 10th at 10 AM.',
                'target_audience': 'staff',
                'category': 'Administrative',
            },
            {
                'title': 'Library Extended Hours',
                'content': 'The library will remain open until 10 PM during the exam period.',
                'target_audience': 'all',
                'category': 'General',
            },
        ]
        
        for ann_data in announcements_data:
            Announcement.objects.get_or_create(
                title=ann_data['title'],
                defaults={
                    'posted_by': staff_user,
                    'content': ann_data['content'],
                    'target_audience': ann_data['target_audience'],
                    'category': ann_data['category'],
                    'expiry_date': timezone.now().date() + timedelta(days=30),
                }
            )
        
        self.stdout.write(self.style.SUCCESS('✓ Created sample announcements'))
        
        self.stdout.write(self.style.SUCCESS('\n=== SAMPLE DATA CREATED ==='))
        self.stdout.write('Admin: admin@scras.maseno.ac.ke / admin123')
        self.stdout.write('Staff: staff1@maseno.ac.ke / staff123')
        self.stdout.write('Student: student1@students.maseno.ac.ke / student123')