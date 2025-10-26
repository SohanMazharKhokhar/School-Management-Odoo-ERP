# -*- coding: utf-8 -*-
{
    'name': "School Management",
    'summary': "Manage students, teachers, classes, and courses.",
    'description': """
        A comprehensive module to manage school operations including student enrollment,
        teacher records, course management, timetabling, fees, and examinations.
    """,
    'author': "Your Name", # Change to your name
    'website': "http://www.yourwebsite.com", # Optional: Change or remove
    'category': 'Education',
    'version': '1.0',
    'depends': ['base', 'mail', 'base_setup'], # <-- CORRECTED    
    'data': [
        'security/ir.model.access.csv',
        'views/student_views.xml',
        'reports/student_report_action.xml',   # <-- ADD THIS LINE
        'reports/student_report_template.xml',
        # Add other view files here later
        'views/teacher_views.xml', # <-- ADD THIS LINE
        'views/subject_views.xml', # <-- ADD THIS LINE
        'views/class_views.xml', # <-- ADD THIS LINE
        'views/course_views.xml', # <-- ADD THIS LINE
        'views/timetable_views.xml', # <-- ADD THIS LINE
        'views/exam_views.xml', # <-- ADD THIS LINE
        'views/fee_type_views.xml', # <-- ADD THIS LINE
        'views/student_fee_views.xml', # <-- ADD THIS LINE
        'views/attendance_views.xml', # <-- ADD THIS LINE
        'views/dashboard_views.xml', # <-- ADD THIS LINE
        'views/attendance_wizard_views.xml', # <-- ADD THIS LINE
        'views/fee_generation_wizard_views.xml', # <-- ADD THIS LINE
        'data/ir_cron_data.xml', # <-- ADD THIS LINE
        'views/payslip_views.xml', # <-- ADD THIS LINE
        'views/school_menus.xml', # We'll create a separate file for main menus
    ],
    'installable': True,
    'application': True, # Mark as a full application
    'license': 'LGPL-3',
}
