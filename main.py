import curses
import json
import os
from secrets import save_api_key
from secrets import load_api_key
from ds import start_chat
from pds import hello
from tools import load_config,clear_screen
from openai import OpenAI,AuthenticationError,APIConnectionError,APIStatusError
api_key = load_api_key()

s1_t = "    1. Sign in with OTECH-Account"
s1_l = "       Usage included with Plus, Pro plans"
c1_t = " >  1. Sign in with OTECH-Account"
c1_l = "       Usage included with Plus, Pro plans"
s2_t = "    2. Provide your own API key"
s2_l = "       Pay for what you use"
c2_t = " >  2. Provide your own API key"
c2_l = "       Pay for what you use"


config = load_config()
model = config["model"]
client_version = config["version"]

def check_api_key(api_key):
    api_key = api_key.strip()

    if not api_key:
        return False, "api-key can't be empty"

    client = OpenAI(
        api_key=api_key,
        base_url="https://api.deepseek.com",
        timeout=15.0,
    )

    try:
        client.chat.completions.create(
            model="deepseek-flash",
            messages=[  #type: ignore
                {
                    "role": "user",
                    "content": "Reply only: OK",
                }
            ],
            max_tokens=1,
        )

        return True, "api-key is valid"

    except AuthenticationError:
        return False, "api-key is invalid"

    except APIConnectionError:
        return False, "internet connection error"

    except APIStatusError as error:
        return False, f"HTTP status code：{error.status_code}"

def main(screen):
    curses.start_color()
    screen.keypad(True)
    curses.init_pair(1, curses.COLOR_BLUE, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK)

    page = "home"
    selected = 1
    logo = r"""
           ___     ____   _       ___
          / _ \   / ___| | |     |_ _|
         | | | | | |     | |      | |
         | |_| | | |___  | |___   | |
          \___/   \____| |_____| |___|
    """
    while True:
        screen.clear()
        for row, line in enumerate(logo.strip("\n").splitlines()):
            screen.addstr(row, 0, line, curses.color_pair(1),)

        color1 = curses.color_pair(2) if selected == 1 else curses.color_pair(3)
        color2 = curses.color_pair(2) if selected == 2 else curses.color_pair(3)
        t1 = c1_t if selected == 1 else s1_t
        l1 = c1_l if selected == 1 else s1_l
        t2 = s2_t if selected == 1 else c2_t
        l2 = s2_l if selected == 1 else c2_l

        screen.addstr(7, 0, "    Welcome to OCLI, OTECH's command-line coding agent",curses.color_pair(3))
        screen.addstr(9, 0, "    Sign in with OTECH-Account to use OCLI as part of your paid plan",curses.color_pair(3))
        screen.addstr(10, 0, "    or connect an API key for usage-based billing",curses.color_pair(3))
        screen.addstr(12, 0, t1, color1)
        screen.addstr(13, 0, l1, color1 | curses.A_DIM)
        screen.addstr(15, 0, t2, color2)
        screen.addstr(16, 0, l2, color2 | curses.A_DIM)
        screen.addstr(18, 0, "    Press Enter to continue",curses.color_pair(3) | curses.A_DIM)
        screen.refresh()

        key = screen.getch()

        if key == curses.KEY_UP:
            selected = 1
        elif key == curses.KEY_DOWN:
            selected = 2
        elif key in (curses.KEY_ENTER, 10, 13):
            return selected
if api_key:
    clear_screen()
    hello()
    print(">_ OTECH CLI")
    print("version:" + client_version)
    print("model:" + model+ "\n")
    print()
    print("Enter -help to see available commands")
    print()
    start_chat(api_key)
else:
    selected = curses.wrapper(main)
    if selected == 1:
        clear_screen()
        print("SORRY")
    elif selected == 2:
        if api_key:
            clear_screen()
            hello()
            print()
            start_chat(api_key)
        else:
            clear_screen()
            hello()
            print()
            print("No API key provided")

            while True:
                api_key = input("Please enter your API key: ")
                is_valid, message = check_api_key(api_key)
                print(message)
                if is_valid:
                    save_api_key(api_key)
                    print("API key has been securely saved to the system keychain.")
                    clear_screen()
                    hello()
                    print(">_ OTECH CLI")
                    print("version:" + client_version)
                    print("model:" + model + "\n")
                    print()
                    print("Enter -help to see available commands")
                    print()
                    start_chat(api_key)
                    break
                else:
                    print("The API key was not saved.")