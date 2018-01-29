import unittest
import datetime
import pytest
from unittest.mock import Mock
from beancount_importers import GeneralImporter, BudgetImporter, BankImporter
from beancount.core.number import D
from beancount.core import amount
from beancount.core import data
from beancount.core import flags


def generate_transaction(
    meta,
    trans_date,
    trans_payee,
    trans_description,
    trans_account,
    trans_amount,
    trans_second_posting_account,
):
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
            trans_second_posting_account,
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
        self.file.name = 'tests/test_data/Budget/budget.csv'
        self.trans_second_posting_account = "Assets:Cash"

    def test_budget_importer_name(self):
        self.assertEqual(self.gi.name(), 'BudgetImporter')

    def test_budget_importer_identify_files(self):
        self.assertTrue(self.gi.identify(self.file))

    def test_budget_import_other_filenames(self):
        self.file.name = 'tests/test_data/Budget/budget.txt'
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
                self.trans_second_posting_account,
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
                self.trans_second_posting_account,
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
                self.trans_second_posting_account,
            ),
            extracted_data[1]
        )


class TestBankImporter(unittest.TestCase):

    def setUp(self):
        self.gi = BankImporter()

        self.file = Mock()
        self.file.name = 'tests/test_data/Bank/Data-credit_card.csv'

    def test_budget_importer_name(self):
        self.assertEqual(self.gi.name(), 'BankImporter')

    def test_budget_importer_identify_files(self):
        self.assertTrue(self.gi.identify(self.file))

    def test_budget_import_other_filenames(self):
        self.file.name = 'tests/test_data/Bank/budget.txt'
        self.assertFalse(self.gi.identify(self.file))

    def test_default_location_of_alias_rules(self):
        self.assertEqual(
            self.gi.alias_rules_path,
            '~/.config/beancount-importers/bank_alias_rules.yml',
        )

    def test_import_alias_rules(self):
        self.gi = BankImporter('tests/test_data/Bank/bank_alias_rules.yml')
        self.gi._import_alias_rules()
        self.assertEqual(
            self.gi.alias_rules[0],
            {
                'regexp': '.*RISEUP.*',
                'account': 'Expenses:Bills:Email',
                'payee': 'Riseup'
            }
        )

    def test_extract_account_method(self):
        self.assertEqual(
            self._extract_account('CREDIT CARD PAYMENT TO RISEUP'),
            'Expenses:Bills:Email',
        )

#    @pytest.mark.skip()
#    def test_budget_importer_general_expense_extract(self):
#        extracted_data = self.gi.extract(self.file)
#        trans_date = datetime.datetime.strptime("18/01/2018", "%d-%m-%Y")
#        trans_account = 'Expenses:Bills:Email'
#        trans_payee = 'Riseup'
#        trans_description = 'CREDIT CARD PAYMENT TO RISEUP'
#        trans_amount = '30'
#        meta = data.new_metadata(self.file.name, 0)
#        self.assertEqual(
#            generate_transaction(
#                meta,
#                trans_date,
#                trans_payee,
#                trans_description,
#                trans_account,
#                trans_amount,
#                trans_second_posting_account,
#            ),
#            extracted_data[0]
#        )
#
#    @pytest.mark.skip()
#    def test_budget_importer_general_assets_extract(self):
#        extracted_data = self.gi.extract(self.file)
#        trans_date = datetime.datetime.fromtimestamp(1478171878)
#        trans_account = 'Assets:Debt:Homer'
#        trans_payee = 'Abuh'
#        trans_description = 'Lollipop'
#        trans_amount = '-10'
#        meta = data.new_metadata(self.file.name, 4)
#        self.assertEqual(
#            generate_transaction(
#                meta,
#                trans_date,
#                trans_payee,
#                trans_description,
#                trans_account,
#                trans_amount,
#                trans_second_posting_account,
#            ),
#            extracted_data[4]
#        )
#
#    @pytest.mark.skip()
#    def test_budget_importer_decimal_amount(self):
#        extracted_data = self.gi.extract(self.file)
#        trans_date = datetime.datetime.fromtimestamp(1478171818)
#        trans_account = 'Expenses:Groceries'
#        trans_payee = 'Salad'
#        trans_description = ''
#        trans_amount = '-2.89'
#        meta = data.new_metadata(self.file.name, 1)
#        self.assertEqual(
#            generate_transaction(
#                meta,
#                trans_date,
#                trans_payee,
#                trans_description,
#                trans_account,
#                trans_amount,
#                trans_second_posting_account,
#            ),
#            extracted_data[1]
#        )


if __name__ == '__main__':
    unittest.main()
