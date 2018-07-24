# -*- coding: utf-8 -*-
# Copyright 2018 Therp BV <http://therp.nl>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from openerp import fields, models


class DeliveryCarrier(models.Model):
    _inherit = 'delivery.carrier'

    code = fields.Char(readonly=True)
    package_type_id = fields.Many2one(
        'stock.quant.package',
        domain=[('code', '!=', False)],
        string='Package Type',
    )
