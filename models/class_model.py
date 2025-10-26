# -*- coding: utf-8 -*-
from odoo import models, fields, api, _  # <-- REQUIRED IMPORTS ADDED
from odoo.exceptions import UserError  # <-- REQUIRED IMPORTS ADDED

class SchoolClass(models.Model):
    _name = "school.class"
    _description = "School Class"
    _inherit = ['mail.thread', 'mail.activity.mixin'] # <-- Added mixin for tracking fields

    name = fields.Char(string="Class Name", required=True, tracking=True,
                       help="E.g., Grade 5 - Section A")
    level = fields.Char(string="Level/Grade", tracking=True, help="E.g., Grade 5")
    section = fields.Char(string="Section", tracking=True, help="E.g., A, B, Blue")
    class_teacher_id = fields.Many2one('school.teacher', string="Class Teacher",
                                       tracking=True,
                                       help="The main teacher responsible for this class.")
    active = fields.Boolean(string="Active", default=True)

    student_ids = fields.One2many('school.student', 'class_id', string="Students")
    subject_ids = fields.Many2many('school.subject', string="Subjects", tracking=True)
    
    # We will use this computed field to show the total number of students
    student_count = fields.Integer(string='Student Count', compute='_compute_student_count', store=True)

    _sql_constraints = [
        ('name_unique', 'unique(name)', 'Class Name must be unique!')
    ]

    @api.depends('student_ids')
    def _compute_student_count(self):
        for record in self:
            record.student_count = len(record.student_ids)


    # The logic below is not directly called by a button, but by the Wizard. 
    # For now, we will leave the logic in the Wizard (fee.generation.wizard)
    # as that is the standard Odoo practice.

    # NOTE: Since the logic is now handled in the Wizard (which collects the inputs), 
    # we don't need a method here with these exact parameters.
    # The Wizard will simply call self.env['school.student.fee'].create(...) directly.