import os
os.system("python -m pip install requests --upgrade")
os.system("cls")

import time
import requests # type: ignore
import ctypes
ctypes.windll.kernel32.SetConsoleTitleW("Webhook Spammer")

webhook_url = input("Please Enter Webhook URL: ")
message = input("Please Enter the Spam Message: ")
os.system("cls")

def spam(webhook_url, message):
    while True:
        try:
            data = requests.post(webhook_url, json={'content': message})
            print(f"Response text: {data.text}")
            print(f"Status Code: {data.status_code}")
        
            if data.status_code == 204:
                print(f"Sent: {message}\n")
            else:
                try:
                    time.sleep(data.json()["retry_after"]/1000)
                except:
                    pass
        except KeyboardInterrupt:
            print("Keyboard Interrupt")

while True:
    spam(webhook_url, message)