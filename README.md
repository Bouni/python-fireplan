# python-fireplan

[![Run tests and lint](https://github.com/Bouni/python-fireplan/actions/workflows/test-and-lint.yaml/badge.svg)](https://github.com/Bouni/python-fireplan/actions/workflows/test-and-lint.yaml)

A python package around the public [fireplan](https://data.fireplan.de/swagger/index.html) API.

## Installation

`pip install python-fireplan`

## Usage

### Alarm

```python
from fireplan import Fireplan

# Fireplan Registration ID
secret = "B75C394B-624526A5"
# Your Division
division = "Musterhausen"

fp = Fireplan(secret, division)

alarmdata =  {
    "alarmtext": "",
    "einsatznrlst": "",
    "strasse": "",
    "hausnummer": "",
    "ort": "",
    "ortsteil": "",
    "objektname": "",
    "koordinaten": "",
    "einsatzstichwort": "",
    "zusatzinfo": "",
    "sonstiges1": "",
    "sonstiges2": "",
    "RIC": "",
    "SubRIC": ""
}

fp.alarm(alarmdata)
```

### Status

```python
from fireplan import Fireplan

secret = "B75C394B-624526A5"
# Your Division
division = "Musterhausen"

fp = Fireplan(secret, division)

statusdata = {
    "FZKennung": "40225588996", 
    "Status": "3"
}

fp.status(statusdata)
```

## Testing

```sh
source .venv/bin/activate # activate venv

python -m pytest # run tests
```

## Notice of Non-Affiliation and Disclaimer

We are not affiliated, associated, authorized, endorsed by, or in any way officially connected with Fireplan, or any of its subsidiaries or its affiliates. The official Fireplan website can be found at https://www.fireplan.de.

The name Fireplan as well as related names, marks, emblems and images are registered trademarks of their respective owners.

