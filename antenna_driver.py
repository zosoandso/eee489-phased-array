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

board = pyfirmata.ArduinoMega('/dev/ttyACM0') # Linux PC for demo
#board = pyfirmata.ArduinoMega('/dev/cu.usbmodem101') # Mac for antenna test
#board = pyfirmata.ArduinoDue('COM?') # Travis' Arduino Due on Windows
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
        shift = '000000000000000000000000' # failsafe return to (0, 90)
    return shift

def do_shift(point: Tuple[float, float]) -> None: # phase shift command
    shift = get_shift(point)
    for i in range(0, len(shift)):
        write(SERIAL, 1) if shift[i] == '1' else write(SERIAL, 0)
        write(CLOCK, 1)
        write(CLOCK, 0)
    write(ENABLE, 1)
    write(ENABLE, 0)
    plot_beam(point)

def check_signal() -> int:
    cmd = "iw wlp6s0 station dump | grep 'signal avg'"
    power = sp.check_output(cmd, shell=True)
    power = power.decode('utf-8')
    power = re.search('-\d\d', power)
    return int(power.group())

def check_ssid(ssid: str) -> bool:
    cmd = 'nmcli dev wifi list --rescan yes | grep '
    cmd += ssid
    check = sp.check_output(cmd, shell=True)
    check = check.decode('utf-8')
    check = re.search(ssid, check)

    if check == None:
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
                        try:
                            check_ssid(ssid)
                        except:
                            print('SSID not found. Attempting next point.')
                        else:
                            return ssid

def connect() -> None:
    ssid = find_ap()
    pw = getpass.getpass('Enter password: ')
    pw = "'" + pw + "'"
    cmd = 'nmcli dev wifi con ' + ssid + ' password ' + pw
    sp.run(cmd, shell=True)

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
