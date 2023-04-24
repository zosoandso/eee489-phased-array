from typing import Tuple

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import subprocess as sp
import getpass
import pyfirmata
import time
import re

PAUSE = 0.005  # 'clock' period
SERIAL = 2     # Arduino pin numbers for SPI bus
CLOCK = 4
ENABLE = 6

#board = pyfirmata.ArduinoMega('/dev/ttyACM0') # Linux PC for demo
board = pyfirmata.ArduinoMega('/dev/cu.usbmodem1401') # Mac for antenna test

data = pd.read_csv('lookangles.csv')

def write(pin: int, logic: int) -> None:
    board.digital[pin].write(logic)
    time.sleep(PAUSE)

def bits(angle: float) -> str:
    return bin(int(angle / 22.5) * 4)[2:].zfill(6)

def test_board() -> None:
    for i in range(0, 17):
        phase = 22.5 * i
        phase %= 360
        phase = bits(phase)
        #print(phase)
        for j in range(0, 6):
            write(SERIAL, 1) if phase[j] == '1' else write(SERIAL, 0)
            write(CLOCK, 1)
            write(CLOCK, 0)
        write(ENABLE, 1)
        write(ENABLE, 0)

def get_shift(point: Tuple[float, float]) -> str:
    for i in range(0, len(data)):
        if data.AZ[i] == point[0] and data.EL[i] == point[1]:
            cmd  = bits(data.J4[i])
            cmd += bits(data.J3[i])
            cmd += bits(data.J2[i])
            cmd += bits(data.J1[i])
            break
    return cmd

def do_shift(point: Tuple[float, float]) -> None: # phase shift command
    shift = get_shift(point)
    for i in range(0, len(shift)):
        write(SERIAL, 1) if shift[i] == '1' else write(SERIAL, 0)
        write(CLOCK, 1)
        write(CLOCK, 0)
    write(ENABLE, 1)
    write(ENABLE, 0)
    plot_beam(point)

def debug() -> None:
    write(SERIAL, 1)
    write(CLOCK, 1)
    write(CLOCK, 0)
    write(SERIAL, 0)
    while True:
        x = input()
        if input == '':
            write(CLOCK, 1)
            write(CLOCK, 0)
        else: break

def check_signal() -> int:
    cmd = "iw wlp6s0 station dump | grep 'signal avg'"
    power = sp.check_output(cmd, shell=True)
    power = power.decode('utf-8')
    power = re.search('-\d\d', power)
    return int(power.group())

def check_ssid(ssid: str) -> bool:
    cmd = 'nmcli dev wifi list --rescan yes | grep '
    cmd += ssid
    try:
        sp.run(cmd, shell=True)
    except:
        return False
    else:
        return True
    
def find_ap() -> str:
    ssid = input('Enter SSID: ')

    while True:
        for i in range(0, len(data)):
            for angle in [0, 45, 90, 135, 180, 225, 270, 315]:
                if data.AZ[i] == angle:
                    if data.EL[i] > 40 and data.EL[i] < 50:
                        point = (data.AZ[i], data.EL[i])
                        do_shift(point)
                        if check_ssid(ssid):
                            return ssid

def connect() -> None:
    ssid = find_ap()
    pw = getpass.getpass('Enter password: ')
    pw = "'" + pw + "'"
    cmd = 'nmcli dev wifi con ' + ssid + ' password ' + pw
    sp.run(cmd, shell=True)

def plot_beam(point: Tuple[float, float]) -> None:
    plt.clf()
    fig = plt.figure()

    ax = fig.add_subplot(projection='polar')
    ax.scatter((point[0] * np.pi) / 180, point[1])

    ax.set_rmax(90)
    ax.set_rticks([15, 30, 45, 60, 75, 90])
    ax.set_theta_offset(np.pi / 2)
    ax.set_rlabel_position(0)
    ax.set_ylim([90, 0])
    ax.grid(True)

    plt.savefig(fname='point.pdf', format='pdf')
