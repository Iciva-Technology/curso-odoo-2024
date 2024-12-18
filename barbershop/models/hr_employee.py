from odoo import models, fields, api

class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    appointment_ids = fields.One2many('barbershop.appointment', 'employee_id', string="Citas")
    number_of_appointments = fields.Integer(string="Cantidad de Citas", compute="_compute_number_of_appointments")
    active = fields.Boolean(string="Activo", default=True)

    @api.depends('appointment_ids')
    def _compute_number_of_appointments(self):
        for employee in self:
            appointments = self.env['barbershop.appointment'].search([('employee_id', '=', employee.id)])
            employee.number_of_appointments = len(appointments)

    def barber_appointment_id(self):
        self.ensure_one()
        active_id = self.env.context.get('employee_id')
        action = self.env["ir.actions.actions"]._for_xml_id("barbershop.barbershop_appointment_action")
        action['domain'] = [('employee_id', '=', active_id)]
        return action
    
    