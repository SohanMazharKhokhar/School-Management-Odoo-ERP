# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError

class FeeGenerationWizard(models.TransientModel):
    _name = 'fee.generation.wizard'
    _description = 'Fee Generation Wizard'

    class_id = fields.Many2one('school.class', string="Target Class", required=True)
    fee_type_id = fields.Many2one('school.fee.type', string="Fee Type", required=True)
    due_date = fields.Date(string="Due Date", required=True, default=fields.Date.today)

    def action_generate_fees(self):
        """ Generate fee records for all students in the selected class. """
        self.ensure_one()

        # Use the existing method structure (simplified for the wizard)
        students = self.class_id.student_ids
        if not students:
            raise UserError(_("The selected class has no students to generate fees for."))

        # Check for existing fees (Optional but good check)
        existing_fees = self.env['school.student.fee'].search_count([
            ('student_id', 'in', students.ids),
            ('due_date', '=', self.due_date),
            ('fee_type_id', '=', self.fee_type_id.id)
        ])
        if existing_fees > 0:
             raise UserError(_("A fee record already exists for some students in this class for the selected fee type and due date."))

        fee_records = []
        for student in students:
            fee_records.append({
                'student_id': student.id,
                'fee_type_id': self.fee_type_id.id,
                'amount_due': self.fee_type_id.amount,
                'due_date': self.due_date,
                'status': 'draft',
            })

        self.env['school.student.fee'].create(fee_records)

        # Return action to view the new fees
        return {
            'name': _("Generated Fees"),
            'type': 'ir.actions.act_window',
            'res_model': 'school.student.fee',
            'view_mode': 'tree,form',
            'domain': [('student_id', 'in', students.ids), ('due_date', '=', self.due_date)],
            'target': 'main',
        }