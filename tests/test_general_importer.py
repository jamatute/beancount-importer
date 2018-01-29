import unittest
import datetime
from unittest.mock import Mock
from beancount_importers import GeneralImporter, BudgetImporter
from beancount.core.number import D
from beancount.core import amount
from beancount.core import data
from beancount.core import flags


def generate_transaction(meta, trans_date, trans_payee, trans_description,
                         trans_account, trans_amount):
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
            amount.Amount(round(-1*D(trans_amount), 2), 'EUR'),
            None, None, None, None
        )
    )
    txn.postings.append(
        data.Posting(
            'Assets:Cash',
            None, None, None, None, None
        )
    )

    return txn


class TestGeneralImporter(unittest.TestCase):
    def setUp(self):
        self.gi = GeneralImporter()

    def test_general_importer_name(self):
        self.assertEqual(self.gi.name(), 'GeneralImporter')


class TestBudgetImporter(unittest.TestCase):
    def setUp(self):
        self.gi = BudgetImporter()

        self.file = Mock()
        self.file.name = 'tests/test_data/budget.csv'

    def test_budget_importer_name(self):
        self.assertEqual(self.gi.name(), 'BudgetImporter')

    def test_budget_importer_identify_files(self):
        self.assertTrue(self.gi.identify(self.file))

    def test_budget_import_other_filenames(self):
        self.file.name = 'tests/test_data/budget.txt'
        self.assertFalse(self.gi.identify(self.file))

    def test_budget_importer_general_expense_extract(self):
        extracted_data = self.gi.extract(self.file)
        trans_date = datetime.datetime.fromtimestamp(1477864184)
        trans_account = 'Expenses:Trips'
        trans_payee = 'NY'
        trans_description = 'awesome_description'
        trans_amount = '-25'
        meta = data.new_metadata(self.file.name, 0)
        self.assertEqual(
            generate_transaction(
                meta,
                trans_date,
                trans_payee,
                trans_description,
                trans_account,
                trans_amount,
            ),
            extracted_data[0]
        )

    def test_budget_importer_general_assets_extract(self):
        extracted_data = self.gi.extract(self.file)
        trans_date = datetime.datetime.fromtimestamp(1478171878)
        trans_account = 'Assets:Debt:Homer'
        trans_payee = 'Abuh'
        trans_description = 'Lollipop'
        trans_amount = '-10'
        meta = data.new_metadata(self.file.name, 4)
        self.assertEqual(
            generate_transaction(
                meta,
                trans_date,
                trans_payee,
                trans_description,
                trans_account,
                trans_amount,
            ),
            extracted_data[4]
        )

    def test_budget_importer_decimal_amount(self):
        extracted_data = self.gi.extract(self.file)
        trans_date = datetime.datetime.fromtimestamp(1478171818)
        trans_account = 'Expenses:Groceries'
        trans_payee = 'Salad'
        trans_description = ''
        trans_amount = '-2.89'
        meta = data.new_metadata(self.file.name, 1)
        self.assertEqual(
            generate_transaction(
                meta,
                trans_date,
                trans_payee,
                trans_description,
                trans_account,
                trans_amount,
            ),
            extracted_data[1]
        )


if __name__ == '__main__':
    unittest.main()
