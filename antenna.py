from typing import Tuple
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import time
import subprocess as sp
import re
import pyfirmata

PAUSE = 0.01  # 'clock' period

board = pyfirmata.ArduinoMega('/dev/cu.usbmodem101')
data = pd.read_csv('lookangles.csv')

def bits(angle: float) -> str:
    return bin(int(angle / 22.5) * 4)[2:].zfill(6)

def get_shift(point: Tuple[float, float]) -> str: # select wanted EL and AZ
    for i in range(0, len(data)):                  # phase shift set
        if data.AZ[i] == point[0] and data.EL[i] == point[1]:
            shift  = bits(data.J4[i])
            shift += bits(data.J3[i])
            shift += bits(data.J2[i])
            shift += bits(data.J1[i])
            break
    return shift

def do_shift(point: Tuple[float, float]) -> None: # phase shift command
    shift = get_shift(point)
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
    plt.ion()
    fig = plt.figure()
    ax = fig.add_subplot(projection='polar')

    ax.scatter(point[0] * np.pi / 180, point[1],
               c=0, s=20, cmap='hsv', alpha=0.75)
    ax.set_rmax(90)
    ax.set_theta_offset(np.pi / 2)
    ax.set_rticks([15, 30, 45, 60, 75, 90]) # less radial ticks
    ax.set_rlabel_position(0) # move radial labels away from plotted line
    ax.invert_yaxis()
    ax.grid(True)

    fig.canvas.draw()
    fig.canvas.flush_events()
