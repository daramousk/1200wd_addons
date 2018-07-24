# -*- coding: utf-8 -*-
# Copyright 2018 Therp BV <https://therp.nl>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from openerp import models, fields


class ServiceLevelOther(models.Model):
    _name = 'service.level.other'

    name = fields.Char()
    code = fields.Char()
    is_default = fields.Char()
