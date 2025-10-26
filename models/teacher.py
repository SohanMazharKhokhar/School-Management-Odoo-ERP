# -*- coding: utf-8 -*-
from odoo import models, fields, api

class SchoolTeacher(models.Model):
    _name = "school.teacher"
    _description = "School Teacher"
    _inherit = ['mail.thread', 'mail.activity.mixin'] # For chatter

    name = fields.Char(string="Name", required=True, tracking=True)
    teacher_id = fields.Char(string="Teacher ID", tracking=True)
    date_of_birth = fields.Date(string="Date of Birth", tracking=True)
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other')
    ], string="Gender", tracking=True)
    contact_phone = fields.Char(string="Phone")
    contact_email = fields.Char(string="Email")
    joining_date = fields.Date(string="Joining Date", default=fields.Date.today, readonly=True)
    active = fields.Boolean(string="Active", default=True, tracking=True)
    
    # Relationships
    payslip_ids = fields.One2many('school.payslip', 'teacher_id', string="Payslips")
    payslip_count = fields.Integer(string='Payslip Count', compute='_compute_payslip_count')
    subject_ids = fields.Many2many('school.subject', string="Subjects Taught", tracking=True)
    
    _sql_constraints = [
        ('teacher_id_unique', 'unique(teacher_id)', 'Teacher ID must be unique!')
    ]

    # **** CORRECTLY INDENTED METHOD ****
    @api.depends('payslip_ids')
    def _compute_payslip_count(self):
        """ Computes the number of payslips for the current teacher. """
        for teacher in self:
            teacher.payslip_count = len(teacher.payslip_ids)

