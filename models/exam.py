# -*- coding: utf-8 -*-
from odoo import models, fields

class SchoolExam(models.Model):
    _name = "school.exam"
    _description = "School Examination"
    _inherit = ['mail.thread'] # Optional: Add chatter

    name = fields.Char(string="Exam Name", required=True, tracking=True,
                       help="E.g., Midterm Exam, Final Exam")
    course_id = fields.Many2one('school.course', string="Course", required=True,
                                tracking=True, ondelete='cascade',
                                help="The specific course this exam is for.")
    exam_date = fields.Datetime(string="Exam Date & Time", required=True, tracking=True)
    total_marks = fields.Float(string="Total Marks", required=True, tracking=True)
    active = fields.Boolean(string="Active", default=True)

    # Related fields for easier access in views/searches
    subject_id = fields.Many2one(related='course_id.subject_id', string="Subject", store=True, readonly=True)
    class_id = fields.Many2one(related='course_id.class_id', string="Class", store=True, readonly=True)
    teacher_id = fields.Many2one(related='course_id.teacher_id', string="Teacher", store=True, readonly=True)

    # Later: Add result_ids = fields.One2many('school.exam.result', 'exam_id', string="Results")
    result_ids = fields.One2many('school.exam.result', 'exam_id', string="Results")