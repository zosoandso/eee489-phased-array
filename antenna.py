from pyfirmata import ArduinoMega
from time import sleep

PAUSE = 0.01

UP = []

board = ArduinoMega('/dev/cu.usbmodem101')

def bits(angle):
    return bin(int(angle / 22.5) * 4)[2:].zfill(6)

def do_zero(): # set all 4 phase shifters to 0
    board.digital[23].write(0)
    for i in range(0,24):
        board.digital[25].write(1)
        sleep(PAUSE)
        board.digital[25].write(0)
        sleep(PAUSE)
    board.digital[27].write(1)
    sleep(PAUSE)
    board.digital[27].write(0)
    sleep(PAUSE)

def do_shift(shift): # phase shifter command function
    for i in range(0,len(shift)):
        if shift[i] == '1':
            board.digital[23].write(1)
            sleep(PAUSE)
        else:
            board.digital[23].write(0)
            sleep(PAUSE) 
        board.digital[25].write(1)
        sleep(PAUSE)
        board.digital[25].write(0)
        sleep(PAUSE)
    board.digital[27].write(1)
    sleep(PAUSE)
    board.digital[27].write(0)
    sleep(PAUSE)
