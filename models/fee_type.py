# -*- coding: utf-8 -*-
from odoo import models, fields

class SchoolFeeType(models.Model):
    _name = "school.fee.type"
    _description = "School Fee Type"
    _inherit = ['mail.thread'] # Optional

    name = fields.Char(string="Fee Name", required=True, tracking=True,
                       help="E.g., Tuition Fee, Bus Fee")
    amount = fields.Float(string="Amount", required=True, tracking=True)
    frequency = fields.Selection([
        ('monthly', 'Monthly'),
        ('quarterly', 'Quarterly'),
        ('semesterly', 'Semesterly'), # Half-yearly
        ('yearly', 'Yearly'),
        ('one_time', 'One Time'),
    ], string="Frequency", required=True, default='monthly', tracking=True)
    active = fields.Boolean(string="Active", default=True)

    # Optional: Add description field
    # description = fields.Text(string="Description")
