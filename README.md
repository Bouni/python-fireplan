# fireplan

![Status](https://github.com/Bouni/python-fireplan/actions/workflows/python-package.yml/badge.svg)

A python package around the public [fireplan](https://www.fireplan.de/) API.

## Installation

`pip install python-fireplan`

## Usage

### Alarm

```python
import fireplan

token = "ABCDEF...."

fp = fireplan.Fireplan(token)

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

token = "ABCDEF...."

fp = fireplan.Fireplan(token)

statusdata = {
    "FZKennung": "40225588996", 
    "Status": "3"
}

fp.status(statusdata)
```
