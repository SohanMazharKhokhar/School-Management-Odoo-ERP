# -*- coding: utf-8 -*-
from odoo import models, fields, api
from dateutil.relativedelta import relativedelta
import datetime

class SchoolStudent(models.Model):
    _name = "school.student"
    _description = "School Student"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string="Name", required=True, tracking=True)
    roll_number = fields.Char(string="Roll Number", tracking=True)
    date_of_birth = fields.Date(string="Date of Birth", tracking=True)
    age = fields.Integer(string="Age", compute='_compute_age', store=True, tracking=False)
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other')
    ], string="Gender", tracking=True)
    contact_phone = fields.Char(string="Phone")
    contact_email = fields.Char(string="Email")
    enrollment_date = fields.Date(string="Enrollment Date", default=fields.Date.today, readonly=True)
    active = fields.Boolean(string="Active", default=True)
    class_id = fields.Many2one('school.class', string="Class", tracking=True)
    partner_id = fields.Many2one('res.partner', string="Related Contact", tracking=True,
                                 help="Link this student to a contact record for external use.")
    
    # n8n/Twilio Field
    parent_mobile = fields.Char(string="Parent Mobile (for SMS)")

    # Attendance Stats
    total_absent_days = fields.Integer(string="Total Absent Days", compute='_compute_attendance_stats', store=False)
    attendance_percentage = fields.Float(string="Attendance (%)", compute='_compute_attendance_stats', store=False, digits=(3, 2))

    _sql_constraints = [
        ('roll_number_unique', 'unique(roll_number)', 'Roll number must be unique!')
    ]

    @api.depends('date_of_birth')
    def _compute_age(self):
        for record in self:
            if record.date_of_birth:
                today = datetime.date.today()
                record.age = relativedelta(today, record.date_of_birth).years
            else:
                record.age = 0

    def _compute_attendance_stats(self):
        """ Compute attendance stats like total absent days and percentage """
        attendance_env = self.env['school.attendance']
        for student in self:
            relevant_attendance = attendance_env.search([
                ('student_id', '=', student.id),
                ('status', '!=', 'excused')
            ])

            absent_count = len(relevant_attendance.filtered(lambda att: att.status == 'absent'))
            attended_count = len(relevant_attendance.filtered(lambda att: att.status in ['present', 'late']))
            total_recorded_days = attended_count + absent_count

            student.total_absent_days = absent_count
            
            if total_recorded_days > 0:
                student.attendance_percentage = (attended_count / total_recorded_days) * 100
            else:
                student.attendance_percentage = 100.0
