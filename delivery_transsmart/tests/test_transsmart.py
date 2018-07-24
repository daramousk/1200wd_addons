# -*- coding: utf-8 -*-
# Copyright 2018 Therp BV <http://therp.nl>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from openerp.tests import TransactionCase
from openerp.tests.common import post_install


@post_install(True)
class TestTranssmart(TransactionCase):

    def setUp(self):
        super(TestTranssmart, self).setUp()

    def test_transsmart(self):
        pass
