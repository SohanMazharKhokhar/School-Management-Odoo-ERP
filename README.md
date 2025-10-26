# School-Management-Odoo-ERP
🏫 School Management System (Odoo 17) - Full-Stack Portfolio Project

This project is a comprehensive, full-stack ERP module built from scratch on Odoo 17. It demonstrates mastery of core Python development, advanced Odoo workflow automation, and critical external API integration, making it suitable for analysis, reporting, and management of educational operations.

🛠️ Technical Highlights

Category

Technology/Concept

Value Demonstrated

Backend Core

Python, Odoo ORM, PostgreSQL

Custom models (school.payslip, school.student) with computed fields for salary, grades, and attendance.

Workflow Automation

Transient Models (Wizards)

Automated bulk creation of Attendance Sheets and Fee Records by class.

External Integration

n8n, Twilio, Gmail

Robust, multi-channel communication via webhooks for fee reminders.

Data Integrity

Model Inheritance, SQL Constraints

Enforcement of unique Teacher IDs/Roll Numbers and proper relational data linking.

Reporting/UX

XML Views (Form, Tree, Search, Smart Buttons)

Payslip status transitions and quick navigation shortcuts on the Teacher form.

Module Structure and Features

The system manages the entire academic and payroll cycle:

1. Core Management

Students, Teachers, Classes, Subjects, Courses: Foundational data entities with full CRUD (Create, Read, Update, Delete) functionality.

Attendance: Records student attendance (school.attendance) and calculates Total Absent Days and Attendance Percentage on the student profile.

Examinations & Results: Schedules exams and records individual marks, automatically calculating Grade (A+, B, etc.) and Percentage.

2. HR & Payroll

Payslips (school.payslip): Features workflow buttons (Confirm, Paid, Cancel, Draft) and computed fields for Net Salary. (The model inherits essential Odoo currency logic for compatibility).

3. Automated Communication (CI/CD Principle)

The system runs a scheduled job to identify fees that are status='due' and due_date is in the past.

Trigger: Odoo Cron Job (model._check_overdue_fees_and_send_reminders()).

Pipeline: Odoo $\rightarrow$ Webhook $\rightarrow$ n8n $\rightarrow$ (Twilio/WhatsApp) AND (Gmail/Email).

Benefit: Ensures critical communication is separated from the ERP core, increasing reliability and speed.

🚀 Setup and Usage

Installation Steps

Clone the Repository: Place the entire school_management folder inside your custom Odoo addons_path.

Ensure Dependencies: Ensure requests is installed in your virtual environment.

Initialization: Restart your Odoo server using the initialization flag to apply all model and data changes:

# Run from your Odoo installation directory
./odoo-venv/bin/odoo -c odoo.conf -d [YOUR_DB_NAME] -i school_management --stop-after-init
