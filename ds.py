import os
import json
import sys

from openai import OpenAI
from datetime import datetime
from pds import hello
from chatsave import chat_save,chat_load
from pathlib import Path
from tools import write_file,safe_file_path
from tools_definitions import TOOL_DEFINITIONS
from secrets import save_api_key,load_api_key,delete_api_key
def get_date_mock():
    return datetime.now().strftime("%Y-%m-%d")

def get_weather_mock(location, date):
    return "Cloudy 7~13°C"

TOOL_CALL_MAP = {
    "get_date": get_date_mock,
    "get_weather": get_weather_mock,
    "write_file": write_file,

}

def run_turn(client,turn, messages,cdir):
    sub_turn = 1
    while True:
        response = client.chat.completions.create(
            model='deepseek-flash',
            messages=[ #type: ignore
                {"role": "system", "content": "你是deepseek，你正在终端中与用户进行交互，不要使用markdown之类的格式，不要使用空白行，回答保持紧凑，少用emoji，回答格式符合命令行" +
                                              "你的当前工作目录是" + cdir
                 },
                *messages,
            ],
            tools=TOOL_DEFINITIONS, #type: ignore
            reasoning_effort="low",
            extra_body={ "thinking": { "type": "enabled" } },
        )
        messages.append(response.choices[0].message.model_dump(exclude_none=True))
        reasoning_content = response.choices[0].message.reasoning_content
        content = response.choices[0].message.content
        tool_calls = response.choices[0].message.tool_calls
        # print(f"Turn {turn}.{sub_turn}\n{reasoning_content=}\n{content=}\n{tool_calls=}")
        if content:
            print("· "+ content)
        if tool_calls is None:
            break
        for tool in tool_calls:
            tool_function = TOOL_CALL_MAP[tool.function.name]
            tool_result = tool_function(**json.loads(tool.function.arguments))
            # print(f"tool result for {tool.function.name}: {tool_result}\n")
            messages.append({
                "role": "tool",
                "tool_call_id": tool.id,
                "content": tool_result,
            })
        sub_turn += 1

def start_chat(api_key):
    messages = chat_load()
    current_dir = str(Path.cwd())
    client = OpenAI(
        api_key=api_key,
        base_url="https://api.deepseek.com",
    )
    turn = 1
    while True:
        chat_input = input("> ")
        print()
        if chat_input == "-help":
            print("-exit -stop the chat\n"
                  "-key reset your api-key\n"
                  "-tools set what tools to use\n")
        elif chat_input == "-exit":
            c = input("Are you sure you want to exit the chat? (y/n):")
            if c.lower() == "y":
                break
            elif c.lower() == "n":
                print("Exit cancelled.\n")
                continue
            else:
                print("Please enter y or n.\n")
                continue
        elif chat_input == "-key":
            c = input("Are you sure you want to reset your api-key? (y/n):")
            if c.lower() == "y":
                if delete_api_key():
                    print("Successfully reset your API key.\n")
                else:
                    print("Failed to reset your API key.\n")
            elif c.lower() == "n":
                print("Reset cancelled.\n")
                continue
            else:
                print("Please enter y or n.\n")
                continue
        else:
            messages.append({"role": "user", "content": chat_input})
            run_turn(client,turn,messages,current_dir)
            chat_save(messages)
            print()
            turn += 1