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
    data = np.loadtxt('lookangles.csv',delimiter=',' ,skiprows=1)
    phase = data[np.nonzero(np.logical_and(data[:,0]==point[0],
                                              data[:,1]==point[1]))][0,2:]
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
    cmd = 'wpa_cli scan && wpa_cli scan_results | grep EEE489Demo'
    power = sp.Popen(cmd, shell=True, stdout=sp.PIPE, stderr=sp.STDOUT)
    power = power.communicate()[0]
    print(power)

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
