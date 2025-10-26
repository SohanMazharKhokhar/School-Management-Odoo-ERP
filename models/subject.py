# -*- coding: utf-8 -*-
from odoo import models, fields

class SchoolSubject(models.Model):
    _name = "school.subject"
    _description = "School Subject"
    _inherit = ['mail.thread'] # Optional: Add chatter if needed

    name = fields.Char(string="Subject Name", required=True, tracking=True)
    code = fields.Char(string="Subject Code", tracking=True)
    # Optional: Add description field
    # description = fields.Text(string="Description")
    active = fields.Boolean(string="Active", default=True)

    # We might link teachers to subjects later
    # teacher_ids = fields.Many2many('school.teacher', string="Teachers")

    _sql_constraints = [
        ('code_unique', 'unique(code)', 'Subject Code must be unique!')
    ]
