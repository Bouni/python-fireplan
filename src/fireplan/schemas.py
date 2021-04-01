ALARM_SCHEMA = {
    "alarmtext": { 
        "type": "string", 
        "default": "",
        "required": True,
        "coerce": str
    },
    "einsatznrlst": { 
        "type": "string", 
        "default": "",
        "required": True,
        "coerce": str
    },
    "strasse": { 
        "type": "string", 
        "default": "",
        "required": True,
        "coerce": str
    },
    "hausnummer": { 
        "type": "string", 
        "default": "",
        "required": True,
        "coerce": str
    },
    "ort": { 
        "type": "string", 
        "default": "",
        "required": True,
        "coerce": str
    },
    "ortsteil": { 
        "type": "string", 
        "default": "",
        "required": True,
        "coerce": str
    },
    "objektname": { 
        "type": "string", 
        "default": "",
        "required": True,
        "coerce": str
    },
    "koordinaten": { 
        "type": "string", 
        "default": "",
        "regex": "^\-?\d+\.\d+,\s?\-?\d+\.\d+$",
        "required": True,
        "coerce": str
    },
    "einsatzstichwort": { 
        "type": "string", 
        "default": "",
        "required": True,
        "coerce": str
    },
    "zusatzinfo": { 
        "type": "string", 
        "default": "",
        "required": True,
        "coerce": str
    },
    "sonstiges1": { 
        "type": "string", 
        "default": "",
        "required": True,
        "coerce": str
    },
    "sonstiges2": { 
        "type": "string", 
        "default": "",
        "required": True,
        "coerce": str
    },
    "RIC": { 
        "type": "string", 
        "default": "",
        "required": True,
        "coerce": str
    },
    "SubRIC": { 
        "type": "string", 
        "default": "",
        "required": True,
        "coerce": str
    },
}

STATUS_SCHEMA = {
    "FZKennung": { 
        "type": "string", 
        "default": "",
        "required": True,
        "coerce": str,
        "empty": False
    },
    "Status": { 
        "type": "string", 
        "default": "",
        "required": True,
        "coerce": str,
        "empty": False
    }
}
