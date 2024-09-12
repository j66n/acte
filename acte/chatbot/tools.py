tools = [
    {
        "type": "function",
        "function": {
            "name": "new_session",
            "strict": True,
            "description": "Start a new App session, and the return value is the session's latest screen.",
        },
    },
    {
        "type": "function",
        "function": {
            "name": "execute",
            "strict": True,
            "description": "Execute one or more action(s), "
                           "and the return value is the session's latest screen.",
            "parameters": {
                "type": "object",
                "properties": {
                    "session_id": {
                        "type": "string",
                    },
                    "actions": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "target_id": {
                                    "type": "string",
                                    "description": "Targeted element's id in the view.",
                                },
                                "action_type": {
                                    "type": "string",
                                    "enum": ["press", "set"],
                                    "description": "press: press the button; "
                                                   "set: set the input field's value"
                                },
                                "value": {
                                    "description": "When the action_type is 'set', "
                                                   "the value is required."
                                                   "The type of value should be consistent with the field schema. "
                                }
                            },
                            "required": ["target_id", "action_type"],
                        },
                    },
                },
                "required": ["session_id", "actions"],
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "display",
            "strict": True,
            "description": "The return value is the session's latest screen.",
            "parameters": {
                "type": "object",
                "properties": {
                    "session_id": {
                        "type": "string",
                    },
                },
                "required": ["session_id"],
            }
        }
    },
]
