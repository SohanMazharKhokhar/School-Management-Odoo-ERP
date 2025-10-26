# -*- coding: utf-8 -*-
from odoo import models, fields, api

class SchoolCourse(models.Model):
    _name = "school.course"
    _description = "School Course Offering"
    _inherit = ['mail.thread'] # Optional: Add chatter

    # Computed field for the name
    name = fields.Char(string="Course Name", compute='_compute_name', store=True, readonly=True)

    subject_id = fields.Many2one('school.subject', string="Subject", required=True, tracking=True)
    class_id = fields.Many2one('school.class', string="Class", required=True, tracking=True)
    teacher_id = fields.Many2one('school.teacher', string="Teacher", tracking=True)
    academic_year = fields.Char(string="Academic Year", tracking=True, help="E.g., 2025-2026")
    active = fields.Boolean(string="Active", default=True)

    # Later: Add fields for timetable/schedule

    _sql_constraints = [
        ('course_unique', 'unique(subject_id, class_id, academic_year)',
         'A course for this subject and class already exists for this academic year!')
    ]

    @api.depends('subject_id', 'class_id', 'teacher_id')
    def _compute_name(self):
        """ Computes a descriptive name, e.g., 'Math - Grade 5 A (Mr. Smith)' """
        for record in self:
            name_parts = []
            if record.subject_id:
                name_parts.append(record.subject_id.name)
            if record.class_id:
                name_parts.append(record.class_id.name)
            # Optional: Add teacher name to course name
            # if record.teacher_id:
            #     name_parts.append(f"({record.teacher_id.name})")

            if name_parts:
                record.name = " - ".join(name_parts)
            else:
                record.name = "New Course"

