# -*- coding: utf-8 -*-
# © 2016 1200 Web Development <http://1200wd.com/>
# © 2017 Therp BV <http://therp.nl>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from openerp import models, fields, api
from transsmart.connection import Connection


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    cost_center_id = fields.Many2one(
        'cost.center',
        string='Delivery Cost Center')
    delivery_cost = fields.Float('Delivery Cost', readonly=True)
    carrier_tracking_url = fields.Char('Carrier Tracking URL')
    company_transsmart_enabled = fields.Boolean(
        related='company_id.transsmart_enabled',
    )

    def _get_service_level_time_id(self):
        self.ensure_one()
        return self.carrier_id.product_id.service_level_time_id.code \
            or self.service_level_time_id or \
            self.env['service.level.time'].browse(int(
                self.env['ir.config_parameter'].get_param(
                    'transsmart_service_level_time_id',
                ))
            )

    service_level_time_id = fields.Many2one(
        'service.level.time',
    )

    @api.multi
    def get_invoice_name(self):
        invoice_name = ''
        if self.sale_id.name:
            invoice_name = self.env['account.invoice'].search([
                ('origin', '=', self.sale_id.name),
            ]).number
        return invoice_name

    def _transsmart_create_shipping(self):
        self.ensure_one()
        document = {
            'reference': self.name,
            'additionalReferences': [
                {'type': 'order', 'value': self.sale_id.name},
                {'type': 'yourReference', 'value': self.sale_id.name},
                {'type': 'other', 'value': self.get_invoice_name()},
                {'type': 'invoice', 'value': self.get_invoice_name()},
            ],
            'addresses': [
                {
                    'type': 'RECV',
                    'name': self.company_id.name,
                    'addressLine1': self.company_id.street,
                    'addressLine2': self.company_id.street2,
                    'zipCode': self.company_id.zip,
                    'city': self.company_id.city,
                    'state': self.company_id.state_id.code,
                    'country': self.company_id.country_id.code,
                    'email': self.company_id.email,
                    'telNo': self.company_id.phone,
                },
                {
                    'type': 'SEND',
                    'name': self.partner_id.name,
                    'addressLine1': self.partner_id.street,
                    'addressLine2': self.partner_id.street2,
                    'zipCode': self.partner_id.zip,
                    'city': self.partner_id.city,
                    'state': self.partner_id.state_id.name,
                    'country': self.partner_id.country_id.code,
                    'contact': self.partner_id.name,
                    'telNo': self.partner_id.phone,
                    'email': self.partner_id.email,
                    'customerNumber': self.partner_id.ref,
                },
            ],
            # for now a single package that contains everything
            'packages': [
                {
                    'measurements':
                        {
                            'length': self.carrier_id.package_type_id.length,
                            'width': self.carrier_id.package_type_id.width,
                            'height': self.carrier_id.package_type_id.height,
                            'weight': self.carrier_id.package_type_id.weight,
                        },
                    'packageType': self.carrier_id.package_type_id.type,
                    'quantity': sum(self.move_lines.mapped('product_uom_qty')),
                    'description': '\n'.join([
                        line.prod.description for line in self.move_lines]),
                }
            ],
            'deliveryNoteInformation': {
                'deliveryNoteLines': [
                    {
                        'hsCode': product.hs_code_id.hs_code or \
                        product.categ_id.hs_code_id.hs_code
                    } for product in self.move_lines.mapped('product_id')
                ]
            },
            'carrier': self.carrier_id.code,
            'value': self.sale_id.amount_total,
            'valueCurrency': 'EUR',
            'serviceLevelTime':
                self._get_service_level_time_id().code,
            'costCenter': self.cost_center_id.code,
        }
        return [document]

    @api.multi
    def action_create_transsmart_document(self):
        ir_config_parameter = self.env['ir.config_parameter']
        account_code = ir_config_parameter.get_param('transsmart_account_code')
        for rec in self:
            document = rec._transsmart_create_shipping()
            connection = self._get_transsmart_connection()
            response = connection.Shipment.book(
                account_code,
                'BOOK',
                document).json()
            carrier = self.env['delivery.carrier'].search(
                [('code', '=', response['carrier'])])
            data = {
                'carrier_id': carrier.id,
                'delivery_cost': response['price'],
                'carrier_tracking_url': response['trackingAndTraceUrl'],
                'date_done': response['pickupDate'],
            }
            rec.write(data)

    def _send_to_transsmart(self):
        return self.company_transsmart_enabled \
            and self.picking_type_id.code == 'outgoing' \
            and self.carrier_id.partner_id.code

    def _get_transsmart_connection(self):
        ir_config_parameter = self.env['ir.config_parameter']
        username = ir_config_parameter.get_param('transsmart_username')
        password = ir_config_parameter.get_param('transsmart_password')
        return Connection().connect(username, password)

    @api.multi
    def _transsmart_get_rates(self):
        ir_config_parameter = self.env['ir.config_parameter']
        account_code = ir_config_parameter.get_param('transsmart_account_code')
        for rec in self:
            connection = rec._get_transsmart_connection()
            response = connection.Rate.calculate(
                account_code,
                rec._create_transsmart_document()).json()
            rec.delivery_cost = sum([
                rate['price'] for rate in response['rates']])

    @api.model
    def create(self, vals):
        result = super(StockPicking, self).create(vals)
        if result._send_to_transsmart():
            result._transsmart_get_rates()
        return result

    def copy(self, default=None):
        if not default:
            default = dict()
        default.update({
            'transsmart_confirmed': False,
            'transsmart_id': 0,
            'delivery_cost': 0,
            'carrier_tracking_url': False,
        })
        return super(StockPicking, self).copy(default=default)
