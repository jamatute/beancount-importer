import os
import sys

# beancount doesn't run from this directory
sys.path.append(os.path.dirname(__file__))

# importers located in the importers directory
from beancount_importers import BudgetImporter

CONFIG = [
    BudgetImporter(),
]
