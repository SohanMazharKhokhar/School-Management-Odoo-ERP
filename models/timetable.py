# -*- coding: utf-8 -*-
from odoo import models, fields, api, _ # Added _ for error messages
from odoo.exceptions import ValidationError

class SchoolTimetable(models.Model):
    _name = "school.timetable"
    _description = "School Timetable Entry"
    _inherit = ['mail.thread'] # Optional

    course_id = fields.Many2one('school.course', string="Course", required=True, tracking=True,
                                help="The specific course offering being scheduled.")
    # Store day as string for easier selection definition
    day_of_week = fields.Selection([
        ('1', 'Monday'),
        ('2', 'Tuesday'),
        ('3', 'Wednesday'),
        ('4', 'Thursday'),
        ('5', 'Friday'),
        ('6', 'Saturday'),
        ('7', 'Sunday'),
    ], string="Day of Week", required=True, tracking=True)

    start_time = fields.Float(string="Start Time", required=True, tracking=True,
                              help="Time in 24-hour format, e.g., 9.5 for 9:30 AM")
    end_time = fields.Float(string="End Time", required=True, tracking=True,
                            help="Time in 24-hour format, e.g., 10.5 for 10:30 AM")
    duration = fields.Float(string="Duration (Hours)", compute='_compute_duration', store=True)

    classroom = fields.Char(string="Classroom", tracking=True)

    # Use related fields to easily access info from the course
    teacher_id = fields.Many2one(related='course_id.teacher_id', string="Teacher", store=True, readonly=True)
    class_id = fields.Many2one(related='course_id.class_id', string="Class", store=True, readonly=True)

    @api.depends('start_time', 'end_time')
    def _compute_duration(self):
        for record in self:
            if record.start_time and record.end_time:
                record.duration = record.end_time - record.start_time
            else:
                record.duration = 0.0

    @api.constrains('start_time', 'end_time')
    def _check_time_order(self):
        for record in self:
            if record.start_time >= record.end_time:
                raise ValidationError(_("End Time must be after Start Time."))

    # Add more complex constraints later if needed to prevent overlaps for
    # the same teacher, class, or classroom at the same time.
