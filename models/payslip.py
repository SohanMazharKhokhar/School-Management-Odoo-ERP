# -*- coding: utf-8 -*-
from odoo import models, fields, api, _

class SchoolPayslip(models.Model):
    _name = "school.payslip"
    _description = "Teacher Payslip"
    _inherit = ['mail.thread', 'mail.activity.mixin'] # <-- ADDED 'base.currency.mixin' to resolve report error
    _order = "date_to desc"

    # Computed field for the name
    name = fields.Char(string="Payslip Reference", compute='_compute_name', store=True, readonly=True)

    teacher_id = fields.Many2one('school.teacher', string="Teacher", required=True, tracking=True)
    date_from = fields.Date(string="Date From", required=True, tracking=True)
    date_to = fields.Date(string="Date To", required=True, tracking=True)

    # Basic financial fields
    basic_salary = fields.Float(string="Basic Salary", tracking=True)
    total_allowances = fields.Float(string="Total Allowances", compute='_compute_total_salary', store=True)
    total_deductions = fields.Float(string="Total Deductions", compute='_compute_total_salary', store=True)
    net_salary = fields.Float(string="Net Salary", compute='_compute_total_salary', store=True, tracking=True)

    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('paid', 'Paid'),
        ('cancelled', 'Cancelled'),
    ], string="Status", default='draft', required=True, tracking=True)


    @api.depends('teacher_id', 'date_to')
    def _compute_name(self):
        """ Generates payslip name: Payslip - [Teacher Name] - [Month Year] """
        for record in self:
            if record.teacher_id and record.date_to:
                teacher_name = record.teacher_id.name
                month_year = record.date_to.strftime("%b %Y")
                record.name = f"Payslip - {teacher_name} - {month_year}"
            else:
                record.name = "New Payslip"

    @api.depends('basic_salary', 'total_allowances', 'total_deductions')
    def _compute_total_salary(self):
        """ Computes the Net Salary """
        for record in self:
            record.total_allowances = 0.0
            record.total_deductions = 0.0
            record.net_salary = record.basic_salary + record.total_allowances - record.total_deductions

    # **** BUTTON METHODS ****

    def action_confirm(self):
        """ Transitions payslip to Confirmed state. """
        for record in self:
            if record.state == 'draft':
                record.state = 'confirmed'
        return True

    def action_paid(self):
        """ Transitions payslip to Paid state. """
        for record in self:
            if record.state == 'confirmed':
                record.state = 'paid'
                record.message_post(body="Payslip marked as Paid.")
        return True

    def action_cancel(self):
        """ Transitions payslip to Cancelled state. """
        for record in self:
            if record.state != 'paid': # Cannot cancel if already paid
                record.state = 'cancelled'
                record.message_post(body="Payslip Cancelled.")
        return True

    def action_draft(self):
        """ Transitions payslip back to Draft state. """
        for record in self:
            if record.state in ['confirmed', 'cancelled']:
                record.state = 'draft'
        return True
