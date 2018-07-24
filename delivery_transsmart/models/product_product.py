# -*- coding: utf-8 -*-
# Copyright 2018 Therp BV <http://therp.nl>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from openerp import fields, models


class ProductProduct(models.Model):
    _inherit = 'product.product'

    service_level_time_id = fields.Many2one(
        'service.level.time',
    )
