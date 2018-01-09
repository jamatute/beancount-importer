import unittest
import datetime
from unittest.mock import Mock
from beancount_importers import GeneralImporter, BudgetImporter


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

    def test_budget_importer_general_extract(self):
        self.extracted_data = self.extract(self.file)
        date = datetime.datetime.fromtimestamp(1477864184)
        account = 'Expenses:Trips'
        description = "NY"
        amount = '25'


if __name__ == '__main__':
    unittest.main()
