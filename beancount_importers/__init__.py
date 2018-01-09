#!/usr/bin/python3

# beancount-importer: Personal collection of beancount importers
#
# Copyright (C) 2018 jamatute <jmm@riseup.net>
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

import os
import datetime
from beancount.ingest import importer


class GeneralImporter(importer.ImporterProtocol):
    def name(self):
        return('GeneralImporter')


class BudgetImporter(GeneralImporter):
    def name(self):
        return('BudgetImporter')

    def identify(self, f):
        if 'budget.csv' in os.path.basename(f.name):
            return True
        else:
            return False

    def extract(self, f):
        entries = []
