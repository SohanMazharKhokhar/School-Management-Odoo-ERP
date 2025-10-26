# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class SchoolExamResult(models.Model):
    _name = "school.exam.result"
    _description = "School Exam Result Entry"
    _rec_name = 'student_id'

    exam_id = fields.Many2one('school.exam', string="Exam", required=True,
                              ondelete='cascade') # Removed tracking
    student_id = fields.Many2one('school.student', string="Student", required=True) # Removed tracking
    marks_obtained = fields.Float(string="Marks Obtained", required=True) # Removed tracking

    total_marks = fields.Float(related='exam_id.total_marks', string="Total Marks",
                               store=True, readonly=True)
    percentage = fields.Float(string="Percentage", compute='_compute_percentage',
                              store=True, readonly=True)

    # **** ADD THESE LINES ****
    grade = fields.Char(string="Grade", compute='_compute_grade', store=True, readonly=True)
    # ***********************

    remarks = fields.Text(string="Remarks") # Added remarks field

    _sql_constraints = [
        ('student_exam_unique', 'unique(exam_id, student_id)',
         'A result for this student and exam already exists!')
    ]

    @api.depends('marks_obtained', 'total_marks')
    def _compute_percentage(self):
        for record in self:
            if record.total_marks > 0:
                record.percentage = (record.marks_obtained / record.total_marks) * 100
            else:
                record.percentage = 0.0

    # **** ADD THIS COMPUTE METHOD ****
    @api.depends('percentage')
    def _compute_grade(self):
        for record in self:
            if record.percentage >= 90:
                record.grade = 'A+'
            elif record.percentage >= 80:
                record.grade = 'A'
            elif record.percentage >= 70:
                record.grade = 'B'
            elif record.percentage >= 60:
                record.grade = 'C'
            elif record.percentage >= 50:
                record.grade = 'D'
            else:
                record.grade = 'F'
    # *********************************

    @api.constrains('marks_obtained', 'total_marks')
    def _check_marks(self):
        # ... (constraint method remains the same) ...
        for record in self:
            if record.marks_obtained < 0:
                 raise ValidationError(_("Marks obtained cannot be negative."))
            if record.marks_obtained > record.total_marks:
                 raise ValidationError(_("Marks obtained cannot exceed total marks (%(total)s).", total=record.total_marks))