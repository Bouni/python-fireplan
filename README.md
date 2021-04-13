# fireplan

![Status](https://github.com/Bouni/python-fireplan/actions/workflows/run-tests.yml/badge.svg)

A python package around the public [fireplan](https://www.fireplan.de/) API.

## Installation

`pip install python-fireplan`

## Usage

### Alarm

```python
import fireplan

# Fireplan Registration ID
secret = "B75C394B-624526A5"
# Your Division
division = "Musterhausen"

fp = fireplan.Fireplan(secret, division)

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
import fireplan

secret = "B75C394B-624526A5"
# Your Division
division = "Musterhausen"

fp = fireplan.Fireplan(secret, division)

statusdata = {
    "FZKennung": "40225588996", 
    "Status": "3"
}

fp.status(statusdata)
```
