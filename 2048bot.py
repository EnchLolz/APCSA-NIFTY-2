#!/usr/bin/env python3
from pynput.keyboard import Controller
import pyautogui
import time
keyboard = Controller()

time.sleep(4)

while True:
    if pyautogui.position() == (0,0):
        break;
    keyboard.press('w')
    keyboard.release('w')
    keyboard.press('a')
    keyboard.release('a')
    keyboard.press('s')
    keyboard.release('s')
    keyboard.press('d')
    keyboard.release('d')
    time.sleep(1/600)
