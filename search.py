from typing import Tuple

import antenna_driver as an

def dumb_search() -> None: # just a test demo don't use
    for i in range(0, len(an.data)):
        point =  (an.data.AZ[i], an.data.EL[i])
        an.do_shift(point)

def quick_search() -> Tuple[float, float]:
    power = -150
    for i in range(0, len(an.data)):
        for angle in [0, 45, 90, 135, 180, 225, 270, 315]:
            if an.data.AZ[i] == angle:
                if an.data.EL[i] > 40 and an.data.EL[i] < 50:
                    point = (an.data.AZ[i], an.data.EL[i])
                    an.do_shift(point)
                    print(point)
                    if an.check_signal() > power:
                        power = an.check_signal()
                        best_point = point
    an.do_shift(best_point)
    an.plot_beam(best_point)
    print(f'\n{best_point}\n')
    return best_point

def search_nearby(point: Tuple[float, float]) -> Tuple[float, float]:
    power = -100
    if point[0] + 15 > 360:
        for i in range(0, len(an.data)):
            if ((an.data.AZ[i] < point[0] + 15 and
                 an.data.AZ[i] > point[0] - 15) or
                 (an.data.AZ[i] < (point[0] + 15) % 360 and
                  an.data.AZ[i] > 0)):
                move = (an.data.AZ[i], an.data.EL[i])
                an.do_shift(move)
                print(move)
                if an.check_signal() > power:
                    power = an.check_signal()
                    best_move = move
    elif point[0] - 15 < 0:
        for i in range(0, len(an.data)):
            if ((an.data.AZ[i] > point[0] - 15 and
                 an.data.AZ[i] < point[0] + 15) or
                 (an.data.AZ[i] > (point[0] - 15) % 360 and
                  an.data.AZ[i] < 360)):
                move = (an.data.AZ[i], an.data.EL[i])
                an.do_shift(move)
                print(move)
                if an.check_signal() > power:
                    power = an.check_signal()
                    best_move = move
    else:
        for i in range(0, len(an.data)):
            if (an.data.AZ[i] > point[0] - 15 and
                 an.data.AZ[i] < point[0] + 15):
                move = (an.data.AZ[i], an.data.EL[i])
                an.do_shift(move)
                print(move)
                if an.check_signal() > power:
                    power = an.check_signal()
                    best_move = move
    an.do_shift(best_move)
    an.plot_beam(best_move)
    print(f'\n{best_move}')
    return best_move
