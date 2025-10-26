# -*- coding: utf-8 -*-
import requests # Library to make HTTP requests
import json
from odoo import models, fields, api, _
import logging # For logging errors

_logger = logging.getLogger(__name__)

class SchoolStudentFeeAutomation(models.Model):
    _inherit = 'school.student.fee' # Inherit the existing model

    @api.model
    def _check_overdue_fees_and_send_reminders(self):
        """
        Scheduled action (cron job) to find overdue fees and trigger n8n webhook.
        This method is called by the ir.cron record in data/ir_cron_data.xml.
        """
        _logger.info("Running scheduled check for overdue fee reminders...")

        # Get n8n webhook URL from system parameters
        webhook_url = self.env['ir.config_parameter'].sudo().get_param('school_management.n8n_fee_webhook_url')
        if not webhook_url:
            _logger.warning("n8n fee reminder webhook URL not set in System Parameters (school_management.n8n_fee_webhook_url). Skipping.")
            return

        # Find fees that are 'due' and past their due date
        today = fields.Date.today()
        overdue_fees = self.search([
            ('status', '=', 'due'),
            ('due_date', '<', today),
        ])

        _logger.info(f"Found {len(overdue_fees)} overdue fees to process.")

        success_count = 0
        fail_count = 0
        for fee in overdue_fees:
            # Ensure student and parent mobile exist
            if not fee.student_id or not fee.student_id.parent_mobile:
                _logger.warning(f"Skipping fee ID {fee.id}: Student or parent mobile missing.")
                fail_count += 1
                continue

            # Prepare data payload for n8n
            # Prepare data payload for n8n
            payload = {
                'student_name': fee.student_id.name,
                'parent_mobile': fee.student_id.parent_mobile, 
                'fee_type': fee.fee_type_id.name,
                'amount': fee.amount_due,
                'due_date': str(fee.due_date),
                'fee_id': fee.id,
                # **** ADD STUDENT EMAIL ****
                'student_email': fee.student_id.contact_email or '', 
                # *************************
            }

            headers = {'Content-Type': 'application/json'}

            try:
                # Send POST request to n8n webhook
                response = requests.post(webhook_url, headers=headers, data=json.dumps(payload), timeout=10)
                response.raise_for_status() # Raise error for bad status codes (4xx or 5xx)
                _logger.info(f"Successfully sent webhook for fee ID {fee.id} to n8n.")
                success_count += 1
            except requests.exceptions.Timeout:
                 _logger.error(f"Timeout sending webhook for fee ID {fee.id} to n8n.")
                 fail_count += 1
            except requests.exceptions.RequestException as e:
                _logger.error(f"Failed to send webhook for fee ID {fee.id} to n8n: {e}")
                fail_count += 1
            except Exception as e:
                 _logger.error(f"An unexpected error occurred processing fee ID {fee.id}: {e}")
                 fail_count += 1

        _logger.info(f"Fee reminder check finished. Success: {success_count}, Failed/Skipped: {fail_count}")
