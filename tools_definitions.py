TOOL_DEFINITIONS = [
    {
        "type": "function",
        "function": {
            "name": "get_date",
            "description": "Get the current date",
            "parameters": {
                "type": "object",
                "properties": {},
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get weather of a location.",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "The city name",
                    },
                    "date": {
                        "type": "string",
                        "description": "Date in YYYY-mm-dd format",
                    },
                },
                "required": ["location", "date"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "write_file",
            "description": "Create or write a text file inside the current working directory only.",
            "parameters": {
                "type": "object",
                "properties": {
                    "filename": {
                        "type": "string",
                        "description": "Relative file path",
                    },
                    "content": {
                        "type": "string",
                        "description": "Text content to write",
                    },
                    "mode": {
                        "type": "string",
                        "enum": ["create", "overwrite", "append"],
                    },
                },
                "required": ["filename", "content"],
            },
        },
    },
]