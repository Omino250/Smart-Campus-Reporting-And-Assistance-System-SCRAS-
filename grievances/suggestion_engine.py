# grievances/suggestion_engine.py

def generate_suggestion(category, description):
    """
    Rule-based suggestion engine that analyzes text and returns appropriate action
    """
    text = description.lower()
    
    # Financial issues
    if 'fees' in text or 'finance' in text or 'money' in text or 'tuition' in text or 'scholarship' in text:
        return "Please visit the Financial Aid Office in Building A, Room 201. Office hours: Mon-Fri 9AM-5PM. You may also email finance@university.edu for assistance."
    
    # Harassment or bullying
    if 'harass' in text or 'bully' in text or 'threat' in text or 'unsafe' in text or 'assault' in text:
        return "This is a serious matter. Please report immediately to the Dean of Students Office (Building B, Room 105) or call the Campus Security hotline: +254-XXX-XXXXXX. Your safety is our priority."
    
    # Academic issues
    if 'exam' in text or 'class' in text or 'grade' in text or 'professor' in text or 'course' in text or 'lecture' in text:
        return "For academic concerns, please consult the Academic Registrar's Office in the Administration Block. You can also reach out to your Department Head or Academic Advisor for guidance."
    
    # Mental health
    if 'mental' in text or 'stress' in text or 'anxiety' in text or 'depression' in text or 'counsel' in text or 'pressure' in text:
        return "Your wellbeing matters. The University Counseling Department is available for confidential support. Location: Student Wellness Center. Call +254-XXX-XXXXXX or email counseling@university.edu to schedule an appointment."
    
    # Accommodation/housing
    if 'hostel' in text or 'accommodation' in text or 'room' in text or 'housing' in text:
        return "Please contact the Housing and Accommodation Office in the Student Affairs Building. Email: housing@university.edu or visit during office hours (Mon-Fri 8AM-4PM)."
    
    # Infrastructure/facilities
    if 'broken' in text or 'repair' in text or 'facility' in text or 'toilet' in text or 'water' in text or 'electricity' in text:
        return "Please report infrastructure issues to the Facilities Management Department. Call the maintenance hotline: +254-XXX-XXXXXX or email facilities@university.edu."
    
    # Default response
    return "Thank you for submitting your issue. Your report has been recorded and relevant staff will review it within 48 hours. You will be contacted if additional information is needed."