from typing import Tuple
import pandas as pd
import time
import pyfirmata

PAUSE = 0.005 # 'clock' period
ZERO = (0, 90) # tuples for test pointing
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
