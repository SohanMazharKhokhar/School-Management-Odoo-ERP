# -*- coding: utf-8 -*-
from odoo import models, fields, api

class SchoolAttendance(models.Model):
    _name = "school.attendance"
    _description = "Student Attendance Record"
    _rec_name = 'student_id' # Show student name by default

    student_id = fields.Many2one('school.student', string="Student", required=True,
                                 ondelete='cascade')
    date = fields.Date(string="Date", required=True, default=fields.Date.today)
    status = fields.Selection([
        ('present', 'Present'),
        ('absent', 'Absent'),
        ('late', 'Late'),
        ('excused', 'Excused Absence'),
    ], string="Status", default='present', required=True)

    # Optional: Link to specific period/course
    timetable_id = fields.Many2one('school.timetable', string="Timetable Slot",
                                   help="Link attendance to a specific class period.")
    # Or alternatively:
    # course_id = fields.Many2one('school.course', string="Course")

    remarks = fields.Text(string="Remarks")

    _sql_constraints = [
        # Prevent duplicate entries for the same student on the same date/timetable slot
        ('student_date_tt_unique', 'unique(student_id, date, timetable_id)',
         'An attendance record for this student on this date/period already exists!')
    ]
