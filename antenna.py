import pyfirmata
import pandas as pd
import time

PAUSE = 0.01 # 'clock' speed
board = pyfirmata.ArduinoMega('/dev/cu.usbmodem101')
data = pd.read_csv('lookangles.csv')

def bits(angle: float) -> str:
    return bin(int(angle / 22.5) * 4)[2:].zfill(6)

def get_angles(index: int) -> str: # select wanted EL and AZ set
    cmd  = bits(data.J4[index])
    cmd += bits(data.J3[index])
    cmd += bits(data.J2[index])
    cmd += bits(data.J1[index])
    return cmd

def do_zero() -> None: # set all 4 phase shifters to 0
    board.digital[23].write(0)
    for i in range(0,24):
        board.digital[25].write(1)
        time.sleep(PAUSE)
        board.digital[25].write(0)
        time.sleep(PAUSE)
    board.digital[27].write(1)
    time.sleep(PAUSE)
    board.digital[27].write(0)
    time.sleep(PAUSE)

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
