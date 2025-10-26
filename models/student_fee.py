# -*- coding: utf-8 -*-
from odoo import models, fields, api

class SchoolStudentFee(models.Model):
    _name = "school.student.fee"
    _description = "Student Fee Record"
    _inherit = ['mail.thread', 'mail.activity.mixin'] # For chatter

    _rec_name = 'student_id' # Show student name by default

    student_id = fields.Many2one('school.student', string="Student", required=True,
                                 tracking=True, ondelete='cascade')
    fee_type_id = fields.Many2one('school.fee.type', string="Fee Type", required=True,
                                  tracking=True)
    # Use a related field initially, but allow manual override
    amount_due = fields.Float(string="Amount Due", required=True, tracking=True)
    due_date = fields.Date(string="Due Date", tracking=True)
    status = fields.Selection([
        ('draft', 'Draft'),
        ('due', 'Due'),
        ('paid', 'Paid'),
        ('cancelled', 'Cancelled'),
    ], string="Status", default='draft', required=True, tracking=True)

    # Related field to easily show frequency
    frequency = fields.Selection(related='fee_type_id.frequency', string="Frequency",
                                 readonly=True, store=True)

    # Optional: Add invoice_id = fields.Many2one('account.move', string="Invoice", readonly=True) later

    _sql_constraints = [
        # Maybe prevent duplicate fee types for the same student on the same due date?
        # ('student_fee_date_unique', 'unique(student_id, fee_type_id, due_date)',
        #  'This fee type is already assigned to the student for this due date.')
    ]

    @api.onchange('fee_type_id')
    def _onchange_fee_type_id(self):
        """ Automatically set amount_due based on fee type """
        if self.fee_type_id:
            self.amount_due = self.fee_type_id.amount
        else:
            self.amount_due = 0.0
    def action_mark_as_due(self):
        """ Sets the fee status to 'Due'. """
        for fee in self:
            if fee.status == 'draft':
                fee.status = 'due'
        return True # Indicate success

    def action_mark_as_paid(self):
        """ Sets the fee status to 'Paid'. """
        for fee in self:
            # You might add checks here later (e.g., only allow if 'Due')
            if fee.status in ['draft', 'due']:
                fee.status = 'paid'
                # Optional: Post a message in the chatter
                fee.message_post(body="Fee marked as Paid.")
        return True

    def action_cancel(self):
        """ Sets the fee status to 'Cancelled'. """
        for fee in self:
            # Add checks if needed (e.g., cannot cancel if already paid?)
            fee.status = 'cancelled'
            fee.message_post(body="Fee Cancelled.")
        return True

    def action_reset_to_draft(self):
        """ Resets the fee status back to 'Draft'. """
        for fee in self:
            # Add checks if needed
            if fee.status in ['cancelled', 'due']: # Allow reset from cancelled or due
                fee.status = 'draft'
                fee.message_post(body="Fee reset to Draft.")
        return True
