# Beancount-importers

Here are a pair of beancount importers:

* For the [F-droid Budget app](https://f-droid.org/en/packages/com.notriddle.budget/)
* For a bank csv

Thank you to [mterwill](https://github.com/mterwill), I took his
[gist](https://gist.github.com/mterwill/7fdcc573dc1aa158648aacd4e33786e8) as
reference

## Features for the Budget importer

* If the Budget envelope starts with `Debt:` it will count as an Asset else it
  will be counted as an Expense
* It will assume `Assets:Cash` as the default second transaction posting

## Features for the bank importer

The CSV must have the following columns:

* empty column
* Execution date of the transfer
* Date of value
* Description
* Import
* Global account amount

The name of the file must be "Data-{{ account_name }}.csv"

## Installation

You can use `pip`

```bash
pip install https://github.com/jamatute/beancount-importers
```

Or clone the repository and install it

```bash
git clone https://github.com/jamatute/beancount-importers
cd beancount-importers
pip3 install -r requirements.txt
python3 setup.py install
```

## Use

```bash
bean-export config.py /path/to/budget.csv
```

## Test

If you want to test the importers run:

```bash
pip3 install -r requirements-tests.txt
pytest
```

To check the coverage run:

```bash
pytest --cov beancount_importers tests
```

## Author

`beancount-importers` was created by [jamatute](https://github.com/jamatute)

## License

GNU General Public License v2.0

See [COPYING](./COPYING) to see the full text.
