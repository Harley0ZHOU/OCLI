import json
import os

def chat_save(message):
    with open("chat.json", 'w', encoding="utf-8") as f:
        json.dump(message, f, ensure_ascii=False, indent=2)

def chat_load():
    if not os.path.exists("chat.json"):
        return []

    with open("chat.json", "r", encoding="utf-8") as file:
        return json.load(file)