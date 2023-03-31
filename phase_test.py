from pyfirmata import ArduinoMega
from time import sleep

PAUSE = 0.01
board = ArduinoMega('/dev/cu.usbmodem101')
runthru = [0,22.5,45,67.5,90,112.5,135,157.5,180,
           202.5,225,247.5,270,292.5,315,337.5,0] # for full angle test

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
#    print(shift)
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

while True:
    ask = input('enter phase shift: ')
    if ask == '':
        break
    elif ask == 'run': # test all angles
        for i in range(0,17):
            do_shift(bin(int(runthru[i]/22.5)*4)[2:].zfill(6))
            sleep(1)
    elif float(ask) % 22.5 != 0 or float(ask) < 0 or float(ask) >= 360:
        print('invalid try again')
    else:
        do_shift(bin(int(ask/22.5)*4)[2:].zfill(6))
        print(f'issued phase shift command: {ask}')
