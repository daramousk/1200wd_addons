# -*- coding: utf-8 -*-
# Copyright 2018 Therp BV <https://therp.nl>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from openerp import api, models


class StockTransferDetails(models.Model):
    _inherit = 'stock.transfer_details'

    @api.multi
    def do_detailed_transfer(self):
        self.ensure_one()
        result = super(StockTransferDetails, self).do_detailed_transfer()
        if result and self.picking_id._send_to_transsmart():
            self.picking_id.action_create_transsmart_document()
        return result
