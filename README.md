# Beancount-importers

Here are a pair of beancount importers:

* For the [F-droid Budget app](https://f-droid.org/en/packages/com.notriddle.budget/)
* For a bank csv

## Features

* Given a list of alias set up the correct name

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

## Test

If you want to test the importers run:

```bash
pip3 install -r requirements-tests.txt
pytest
```

## Author

`kernel_config` was created by [jamatute](https://github.com/jamatute)

## License
GNU General Public License v2.0

See [COPYING](./COPYING) to see the full text.
