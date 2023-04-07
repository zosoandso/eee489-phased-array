from typing import Tuple

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import subprocess as sp
import pyfirmata
import time
import re

PAUSE = 0.001  # 'clock' period
SERIAL = 2
CLOCK = 4
ENABLE = 6

board = pyfirmata.ArduinoMega('/dev/ttyACM0') # linux
#board = pyfirmata.ArduinoMega('/dev/cu.usbmodem101') # mac
#board = pyfirmata.ArduinoDue('COM') # travis' arduino on windows
data = pd.read_csv('lookangles.csv')

def write(pin: int, logic: int) -> None:
    board.digital[pin].write(logic)
    time.sleep(PAUSE)

def bits(angle: float) -> str:
    return bin(int(angle / 22.5) * 4)[2:].zfill(6)

def get_shift(point: Tuple[float, float]) -> str: # select wanted EL and AZ
    newData = np.loadtxt('lookangles.csv',delimiter=',' ,skiprows=1)
    phase = newData[np.nonzero(np.logical_and(newData[:,0]==point[0],
                                              newData[:,1]==point[1]))][0,2:]
    if phase.shape[0] > 0:
        shift  = bits(phase[0])
        shift += bits(phase[1])
        shift += bits(phase[2])
        shift += bits(phase[3])
    else:
        shift = '000000000000000000000000'
    return shift

def do_shift(point: Tuple[float, float]) -> None: # phase shift command
    shift = get_shift(point)
    for i in range(0, len(shift)):
        write(SERIAL, 1) if shift[i] == '1' else write(SERIAL, 0)
        write(CLOCK, 1)
        write(CLOCK, 0)
    write(ENABLE, 1)
    write(ENABLE, 0)

def check_signal() -> int:
    power = sp.check_output(['iw', 'wlp6s0', 'station', 'dump'])
    power = power.decode()
    power = re.search('signal avg:\t-\d\d', power)
    power = re.search('-\d\d', power.group())
    return int(power.group())

def get_rssi_mac() -> int:
    power = sp.check_output(['airport', '-I'])
    power = power.decode('utf-8')
    match = re.search('-\d\d', power)
    return int(match.group())

def plot_beam(point: Tuple[float, float]) -> None:
    plt.clf()

    ax = plt.subplot(111, projection='polar')
    ax.scatter((point[0] * np.pi) / 180, point[1])
    ax.set_rmax(90)
    ax.set_rticks([15, 30, 45, 60, 75, 90])
    ax.set_theta_offset(np.pi / 2)
    ax.set_rlabel_position(0)
    ax.set_ylim([90, 0])
    ax.grid(True)

    plt.savefig(fname='point.pdf', format='pdf')
