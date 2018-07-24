# -*- coding: utf-8 -*-
# Copyright 2018 Therp BV <https://therp.nl>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from openerp import fields, models


class CostCenter(models.Model):
    _name = 'cost.center'

    name = fields.Char()
    code = fields.Char()
    description = fields.Char()
    is_default = fields.Boolean()
