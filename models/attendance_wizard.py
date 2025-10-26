# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError

class SchoolAttendanceWizard(models.TransientModel):
    _name = "school.attendance.wizard"
    _description = "Attendance Registration Wizard"

    class_id = fields.Many2one('school.class', string="Class", required=True)
    date = fields.Date(string="Date", required=True, default=fields.Date.today)
    
    # ADDED THIS RELATED FIELD
    student_ids = fields.One2many(
        'school.student',
        related='class_id.student_ids',
        string="Students in Class",
        readonly=True
    )

    def action_create_attendance(self):
        """ Creates a present attendance record for every student in the selected class."""
        self.ensure_one()

        # UPDATED TO USE self.student_ids
        students = self.student_ids
        if not students:
            raise UserError(_("The selected class has no students to register attendance for."))

        # 2. Check for duplicate entries
        duplicate_check = self.env['school.attendance'].search([
            ('date', '=', self.date),
            ('student_id', 'in', students.ids)
            # Add timetable_id check if you use period-based attendance
        ])
        if duplicate_check:
            # If any record exists for that date, we stop and let the user view/edit manually
            raise UserError(_("Attendance records for this class on this date already exist. Please manage them manually from the Attendance menu."))

        # 3. Create a 'Present' record for each student
        attendance_list = []
        for student in students: # Iterates over self.student_ids now
            attendance_list.append({
                'student_id': student.id,
                'date': self.date,
                'status': 'present', # Default to Present, user can edit in the list view
                # 'timetable_id': False, # Assuming daily attendance for now
            })

        # Create all records in one batch
        self.env['school.attendance'].create(attendance_list)

        # 4. Return an action to view the newly created attendance records (optional but useful)
        return {
            'name': _("Attendance Records Created"),
            'type': 'ir.actions.act_window',
            'res_model': 'school.attendance',
            'view_mode': 'tree,form',
            'domain': [('date', '=', self.date), ('student_id', 'in', students.ids)],
            'target': 'main', # Open in the main content area
        }