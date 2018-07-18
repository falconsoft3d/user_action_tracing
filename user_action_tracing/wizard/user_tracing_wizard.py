# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError

class UserTracingWizard(models.TransientModel):
    _name = 'user.tracing.wizard'

    model_id = fields.Many2one('ir.model', 'Model', required=True, domain="[('transient','=',False)]")
    registry = fields.Integer('ID de Reg',required=True)
    lines = fields.One2many('user.tracing.wizard.line','wizard_id','Resultado')

    @api.onchange('model_id','registry')
    def show_result(self):
        if self.model_id and self.registry:
            records = self.env[self.model_id.model].browse(self.registry)
            self.lines = [(0,0,{\
                'create_user_id': x.create_uid.id,\
                'record_id': x.id,\
                'creation_date': x.create_date,\
                'write_user_id': x.write_uid,\
                'edition_date': x.write_date,\
            }) for x in records]

class UserTracingWizardLine(models.TransientModel):
    _name = 'user.tracing.wizard.line'

    wizard_id = fields.Many2one('user.tracing.wizard', 'Wizard')
    record_id = fields.Integer('ID')
    creation_date = fields.Datetime('Date Create')
    create_user_id = fields.Many2one('res.users', 'Usuario Create')
    edition_date = fields.Datetime('Fecha Edit')
    write_user_id = fields.Many2one('res.users', 'Usuario Edit')
