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
import re
import csv
import datetime
from beancount.ingest import importer
from beancount.core import amount
from beancount.core import data
from beancount.core import flags
from beancount.core.number import D


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
        with open(f.name, 'r') as f:
            for index, row in enumerate(csv.reader(f)):
                meta = data.new_metadata(f.name, index)
                # Budget timestamp has milisecond value that we need to strip
                # so that datetime can parse it -> [:-3]
                trans_date = datetime.datetime.fromtimestamp(float(row[0][:-3]))
                trans_account = row[1]
                if re.match('Debt:*', trans_account):
                    trans_account = 'Assets:{}'.format(trans_account)
                else:
                    trans_account = 'Expenses:{}'.format(trans_account)
                trans_payee = row[3].split(':')[0]
                trans_description = ' '.join(row[3].split(':')[1:])
                trans_amount = float(row[2]) / 100
                txn = data.Transaction(
                    meta=meta,
                    date=trans_date,
                    flag=flags.FLAG_OKAY,
                    payee=trans_payee,
                    narration=trans_description,
                    tags=set(),
                    links=set(),
                    postings=[],
                )

                txn.postings.append(
                    data.Posting(
                        trans_account,
                        amount.Amount(D(trans_amount), 'EUR'),
                        None, None, None, None
                    )
                )

                entries.append(txn)
        return entries
