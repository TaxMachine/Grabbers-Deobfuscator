import os
import sys

from telegram import Telegram # type: ignore
from webhookspammer import Webhook # type: ignore

def updateDisplayDiscord(index: int, discord: Webhook):
    os.system('clear' if sys.platform == 'nt' else 'cls')
    print(f"""
  +--------------------------------------------------+
    Webhook name -> {discord.name}
  +--------------------------------------------------+
     Spammed
    +-------+
     {index}
    +-------+
""")


def updateDisplayTelegram(index: int, telegram: Telegram):
    os.system('clear' if sys.platform == 'nt' else 'cls')
    print(f"""
    +--------------------------------------------------+
     Bot username -> {telegram.username}
     Bot first name -> {telegram.firstName}
     Can dump messages? -> {telegram.dump}
    +--------------------------------------------------+
     Spammed
    +-------+
     {index}
    +-------+
""")
