# grievances/suggestion_engine.py

def generate_suggestion(request_type, description):
    """
    Enhanced rule-based suggestion engine
    Updated to match new request types and provide detailed suggestions
    """
    text = description.lower()
    
    # ========================================
    # MAINTENANCE REQUESTS
    # ========================================
    if request_type == 'maintenance' or any(word in text for word in [
        'broken', 'repair', 'fix', 'damaged', 'leak', 'toilet', 
        'water', 'electricity', 'door', 'window', 'furniture'
    ]):
        return """
        Facilities Management Department
        
        Please report this maintenance issue to the Facilities Management Department.
        
        Contact Information:
        - Location: Administration Block, Ground Floor
        - Phone: +254-057-351622 Ext. 2045
        - Email: facilities@maseno.ac.ke
        - Emergency Hotline: +254-700-000-001 (24/7)
        
        Next Steps:
        1. Your request has been logged with ID for tracking
        2. Maintenance team will assess the issue within 24 hours
        3. Urgent repairs (water, electricity) prioritized immediately
        4. You will receive status updates via email/SMS
        
        Average Response Time: 24-48 hours for standard repairs
        """
    
    # ========================================
    # ACADEMIC REQUESTS
    # ========================================
    if request_type == 'academic' or any(word in text for word in [
        'exam', 'class', 'grade', 'marks', 'course', 'lecturer', 
        'professor', 'unit', 'timetable', 'registration', 'transcript'
    ]):
        return """
        Academic Registrar's Office
        
        For academic-related issues, please consult the Academic Registrar's Office.
        
        Contact Information:
        - Location: Administration Block, 1st Floor
        - Phone: +254-057-351622 Ext. 2010
        - Email: registrar@maseno.ac.ke
        - Office Hours: Monday-Friday, 8:00 AM - 5:00 PM
        
        Services Available:
        - Course registration issues
        - Grade appeals and corrections
        - Transcript requests
        - Academic calendar inquiries
        - Transfer and deferment applications
        
        You may also contact:
        - Your Department Head for course-specific issues
        - Academic Advisor for program guidance
        - Dean of Students for general academic support
        
        Processing Time: 3-5 working days for most academic requests
        """
    
    # ========================================
    # HARASSMENT CASES
    # ========================================
    if request_type == 'harassment' or any(word in text for word in [
        'harass', 'bully', 'threat', 'assault', 'abuse', 'unsafe', 
        'violence', 'discriminat', 'intimidat'
    ]):
        return """
        ⚠️ URGENT: Report to Dean of Students Office Immediately
        
        This is a serious matter. Your safety and wellbeing are our top priority.
        
        IMMEDIATE ACTION REQUIRED:
        
        Dean of Students Office:
        - Location: Student Affairs Building, Room 105
        - Phone: +254-057-351622 Ext. 2030
        - Email: deanofstudents@maseno.ac.ke
        - Emergency: +254-700-000-002 (24/7 Security Hotline)
        
        Campus Security:
        - Main Gate Security Office
        - Emergency: +254-700-000-003
        - Available 24/7
        
        Additional Support:
        - University Counseling Center (confidential support)
        - Gender-Based Violence Response Unit
        - Legal Aid Clinic (for serious cases)
        
        **Your Rights:**
        - All reports are treated with strict confidentiality
        - You have the right to protection and support
        - The university has zero tolerance for harassment
        - You will not face retaliation for reporting
        
        If you are in immediate danger, call Campus Security: +254-700-000-003
        """
    
    # ========================================
    # FINANCIAL ISSUES
    # ========================================
    if request_type == 'financial' or any(word in text for word in [
        'fees', 'finance', 'money', 'tuition', 'scholarship', 'bursary',
        'loan', 'payment', 'bank', 'helb', 'funding'
    ]):
        return """
        Financial Aid Office
        
        For all financial and fees-related matters, please visit the Financial Aid Office.
        
        Contact Information:
        - Location: Administration Block, Ground Floor, Room 15
        - Phone: +254-057-351622 Ext. 2025
        - Email: finance@maseno.ac.ke
        - Office Hours: Monday-Friday, 8:00 AM - 4:00 PM
        
        Services Offered:
        - Fee payment plans and arrangements
        - Scholarship and bursary applications
        - HELB (Higher Education Loans Board) inquiries
        - Fee statements and receipts
        - Financial clearance for graduation
        
        Required Documents:
        - Student ID
        - Admission letter
        - Fee structure
        - Bank payment slips (if applicable)
        
        Payment Options:
        - Bank deposits (Account details at Finance Office)
        - M-PESA Paybill: 123456 (Account: Student ID)
        - Online portal: portal.maseno.ac.ke
        
        Processing Time: Fee queries resolved within 2-3 working days
        """
    
    # ========================================
    # MENTAL HEALTH & COUNSELING
    # ========================================
    if request_type == 'mental' or any(word in text for word in [
        'stress', 'anxiety', 'depression', 'mental', 'counsel', 
        'pressure', 'overwhelm', 'sad', 'worry', 'panic', 'suicide'
    ]):
        return """
        University Counseling Department
        
        Your mental health and wellbeing matter. Professional, confidential support is available.
        
        Counseling Services:
        - Location: College Campus opposite transport department
        - Phone: 0769625499
        - Email: counseling@maseno.ac.ke
        - Crisis Hotline: 0745481416 (24/7)
        
        Services Available:
        - Individual counseling sessions
        - Group therapy and support groups
        - Stress management workshops
        - Academic coaching and time management
        - Crisis intervention (immediate support)
        
        How to Access:
        1. Walk-in during office hours (Mon-Fri, 8 AM - 5 PM)
        2. Call to schedule an appointment
        3. For emergencies, call the crisis hotline immediately
        
        Confidentiality Guarantee:
        - All counseling sessions are 100% confidential
        - No information shared without your consent
        - Safe, non-judgmental environment
        
        Additional Resources:
        - Peer Support Groups: Every Wednesday 4-6 PM
        - Mental Health Awareness Talks: Monthly
        - Online resources: Maseno University Counselling Services Channel
        
        If you're in crisis or having thoughts of self-harm, please call  0745481416 immediately or visit the nearest University hospital.
        
        You are not alone. Help is available💚
        """
    
    # ========================================
    # IT SUPPORT
    # ========================================
    if request_type == 'it' or any(word in text for word in [
        'computer', 'laptop', 'internet', 'wifi', 'portal', 'password',
        'email', 'login', 'system', 'software', 'printer', 'network'
    ]):
        return """
        ICT Department
        
        For all IT and technical support issues, contact the ICT Department.
        
        Contact Information:
        - Location: ICT Center, Near Main Library
        - Phone: +254-057-351622 Ext. 2050
        - Email: ict@maseno.ac.ke
        - Help Desk: helpdesk@maseno.ac.ke
        - Office Hours: Monday-Friday, 8:00 AM - 5:00 PM
        
        Services Offered:
        - Student portal access and password resets
        - University email setup (@students.maseno.ac.ke)
        - WiFi connectivity issues
        - Computer lab support
        - Online learning platform (Moodle) support
        - Software installation assistance
        
        Self-Service Options:
        - Password Reset: portal.maseno.ac.ke/reset
        - WiFi Setup Guide: ict.maseno.ac.ke/wifi-setup
        - Email Configuration: ict.maseno.ac.ke/email-help
        
        Common Solutions:
        - Portal Login: Use Student ID as username
        - WiFi Network: Maseno-Student (Password: Your Student ID)
        - Browser Issues: Try clearing cache or use Chrome/Firefox
        
        Response Time: Most issues resolved within 24 hours
        """
    
    # ========================================
    # ADMINISTRATIVE REQUESTS
    # ========================================
    if request_type == 'administrative' or any(word in text for word in [
        'id', 'card', 'clearance', 'letter', 'document', 'certificate',
        'recommendation', 'verification', 'hostel', 'accommodation'
    ]):
        return """
        Student Affairs Office
        
        For administrative services and general student matters.
        
        Contact Information:
        - Location: Student Affairs Building
        - Phone: +254-057-351622 Ext. 2035
        - Email: studentaffairs@maseno.ac.ke
        - Office Hours: Monday-Friday, 8:00 AM - 5:00 PM
        
        Services Available:
        - Student ID card issuance and replacement
        - Clearance letters
        - Introduction and recommendation letters
        - Verification of student status
        - Hostel and accommodation services
        - Student organization registration
        - Event approval and permits
        
        Required Documents:
        - Valid student ID (or admission letter)
        - Fee payment receipt
        - Passport photo (for ID cards)
        
        Processing Times:
        - ID Cards: 3-5 working days
        - Letters: 1-2 working days
        - Clearance: 2-3 working days
        
        Hostel Matters:
        - Housing Office: Same building, Room 20
        - Email: housing@maseno.ac.ke
        - Allocation, maintenance, and accommodation issues
        """
    
    # ========================================
    # DEFAULT/OTHER
    # ========================================
    return """
    Request Received and Under Review
    
    Thank you for submitting your request through UniServe.
    
    What Happens Next:
    1. Your request has been logged and assigned a tracking ID
    2. It will be reviewed by the appropriate department within 48 hours
    3. You will receive updates via email and in-app notifications
    4. A staff member may contact you for additional information
    
    Track Your Request:
    - View status updates in the "My Requests" section
    - You'll be notified of any status changes
    - Average resolution time: 3-5 working days
    
    Need Immediate Assistance?
    
    Dean of Students Office:
    - Phone: +254-057-351622 Ext. 2030
    - Email: deanofstudents@maseno.ac.ke
    
    Student Affairs:
    - Phone: +254-057-351622 Ext. 2035
    - Email: studentaffairs@maseno.ac.ke
    
    Emergency Services:
    - Campus Security: +254-700-000-003 (24/7)
    - Medical Emergency: +254-700-000-005 (24/7)
    
    Your issue is important to us. We're here to help! 🎓
    """