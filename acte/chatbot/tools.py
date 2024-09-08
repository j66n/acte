tools = [
    {
        "type": "function",
        "function": {
            "name": "new_session",
            "strict": True,
            "description": "Start a new App session, then display the session's latest screen.",
        },
    },
    {
        "type": "function",
        "function": {
            "name": "execute",
            "strict": True,
            "description": "Execute one or more action(s), then display the session's latest screen.",
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
                                    "description": "press: press the button;"
                                                   "set: set the input field's value"
                                },
                                "value": {
                                    "description": "When the action_type is 'input', the value is the input value.",
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
            "description": "Display the session's latest screen.",
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
