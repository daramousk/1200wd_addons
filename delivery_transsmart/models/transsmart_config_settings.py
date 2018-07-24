# -*- coding: utf-8 -*-
# © 2015-2017 1200wd  <http://www.1200wd.com>
# © 2017 Therp BV <http://therp.nl>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from openerp import models, fields, api


class TranssmartConfigSettings(models.TransientModel):
    _name = 'transsmart.config.settings'
    _inherit = 'res.config.settings'

    url = fields.Char(required=True)
    username = fields.Char(required=True)
    password = fields.Char(required=True)
    account_code = fields.Char(required=True)

    @api.multi
    def get_default_transsmart(self):
        self.ensure_one()
        ir_config_parameter = self.env['ir.config_parameter']
        url = ir_config_parameter.get_param('transsmart_url')
        username = ir_config_parameter.get_param('transsmart_username')
        password = ir_config_parameter.get_param('transsmart_password')
        account_code = ir_config_parameter.get_param('transsmart_account_code')
        return {
            'url': url,
            'username': username,
            'password': password,
            'account_code': account_code,
        }

    @api.multi
    def set_transsmart_defaults(self):
        self.ensure_one()
        ir_config_parameter = self.env['ir.config_parameter']
        ir_config_parameter.set_param('transsmart_url', self.url)
        ir_config_parameter.set_param('transsmart_username', self.username)
        ir_config_parameter.set_param('transsmart_password', self.password)
        ir_config_parameter.set_param(
            'transsmart_account_code',
            self.account_code,
        )
