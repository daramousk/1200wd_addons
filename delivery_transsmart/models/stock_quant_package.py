# -*- coding: utf-8 -*-
# © 2017 Therp BV <http://therp.nl>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from openerp import fields, models


class StockQuantPackage(models.Model):
    _inherit = 'stock.quant.package'

    code = fields.Char(readonly=True)
    is_default = fields.Char(readonly=True)
    _type = fields.Char(readonly=True)
    linear_uom = fields.Char(readonly=True)
    mass_uom = fields.Char(readonly=True)
    length = fields.Float(readonly=True)
    width = fields.Float(readonly=True)
    height = fields.Float(readonly=True)
    weight = fields.Float(readonly=True)
