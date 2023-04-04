from typing import Tuple
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import time
import subprocess as sp
import re
import pyfirmata

PAUSE = 0.005  # 'clock' period
ZERO = (0, 90) # tuples for test pointing (azimuth, elevation)
UP = (0, 60)
LEFT = (90, 83)
RIGHT = (270, 82.8)
UP_L = (45, 45)
UP_R = (315, 45)

board = pyfirmata.ArduinoMega('/dev/cu.usbmodem101')
data = pd.read_csv('lookangles.csv')

def bits(angle: float) -> str:
    return bin(int(angle / 22.5) * 4)[2:].zfill(6)

def get_angles(point: Tuple[float, float]) -> str: # select wanted EL and AZ
    for i in range(0, len(data)):                  # phase shift set
        if data.AZ[i] == point[0] and data.EL[i] == point[1]:
            cmd  = bits(data.J4[i])
            cmd += bits(data.J3[i])
            cmd += bits(data.J2[i])
            cmd += bits(data.J1[i])
            break
    return cmd

def do_shift(shift: str) -> None: # phase shifter command function
    for i in range(0,len(shift)):
        if shift[i] == '1':
            board.digital[23].write(1)
            time.sleep(PAUSE)
        else:
            board.digital[23].write(0)
            time.sleep(PAUSE) 
        board.digital[25].write(1)
        time.sleep(PAUSE)
        board.digital[25].write(0)
        time.sleep(PAUSE)
    board.digital[27].write(1)
    time.sleep(PAUSE)
    board.digital[27].write(0)
    time.sleep(PAUSE)

def get_rssi() -> int: # get rssi on lucas' linux pc
    power = sp.check_output(['iwconfig', 'wlp6s0'])
    power = power.decode('utf-8')
    match = re.search('-\d\d', power)
    return int(match.group())

def plot_beam(point: Tuple[float, float]) -> None:
    plt.close('all')
    
    fig = plt.figure()
    ax = fig.add_subplot(projection='polar')
    ax.scatter(point[0] * np.pi / 180, point[1],
               c=0, s=20, cmap='hsv', alpha=0.75)
    ax.set_rmax(90)
    ax.set_theta_offset(np.pi / 2)
    ax.set_rticks([15, 30, 45, 60, 75, 90]) # less radial ticks
    ax.set_rlabel_position(0) # move radial labels away from plotted line
    ax.grid(True)

    plt.show()
