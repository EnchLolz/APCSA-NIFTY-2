# APCSA NIFTY PROJECT #2
## 2048 GAME

[![Build Status](https://travis-ci.org/joemccann/dillinger.svg?branch=master)](https://travis-ci.org/joemccann/dillinger)

This is my second extra credit submission for APCSA

- [2048 GAME](http://nifty.stanford.edu/2017/mishra-2048/)
- Coded in Python3
- Works on Mac and Windows
- Main game requires **pygame** and **random** libraries
- Auto *WASD* bot requires **pynput**, **pyautogui**, and **time** libraries

---

## Features


- Beautiful UI: nice pastel colors + best font (comic sans)
- Keeps track of score and time
- Minimalistic win, lose, and home screen
- Changable grid dimensions and winning score
- Autoclicker for *WASD* (external)
- Optimized calculations
- Very modular

---

## Controls
- **WASD** or **Arrow Keys** to move **up**, **left**, **down**, **right** 
- **Space** button to exit of win, lose, and home screens

---

## How to Use
#### Main Game
Change user settings (lines 5-9)
```py
#user settings 
FPS = 60 
horizontal = 4
vertical = 4
win_score = 11
```
- FPS: FPS
- horizontal: number of horizontal tiles in a row
- vertical: number of vertical tiles in a row
- win_score: score needed to reach to win (log2)
- default settings are shown above

Run the python file

#### WASD Bot

Run the python file

- 4 second delay before start
- must be on game window
- move cursor to top left corner of screen to stop
- be careful, don't mess up your computer
- isn't helpful on grids smaller than 5x5

---

## Images
![All Colors](https://cdn.discordapp.com/attachments/958055074947543113/1050192390406819950/Screen_Shot_2022-12-07_at_3.29.32_PM.png)
![Home Screen](https://cdn.discordapp.com/attachments/958055074947543113/1050190233360146462/Screen_Shot_2022-12-07_at_3.20.58_PM.png)
![Lose Screen](https://cdn.discordapp.com/attachments/958055074947543113/1050202091244769370/Screen_Shot_2022-12-07_at_4.08.05_PM.png)
