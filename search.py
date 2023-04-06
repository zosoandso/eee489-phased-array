from typing import Tuple
import antenna as an

def dumb_search() -> None: # just a test demo don't use
    for i in range(0, len(an.data)):
        point =  (an.data.AZ[i], an.data.EL[i])
        an.do_shift(point)
        an.plot_beam(point)

def quick_search() -> Tuple[float, float]:
    power = -100
    best_point = (0, 0)
    for i in range(0, len(an.data)):
        for angle in [0, 45, 90, 135, 180, 225, 270, 315]:
            if an.data.AZ[i] == angle:
                if an.data.EL[i] > 40 and an.data.EL[i] < 50:
                    point = (an.data.AZ[i], an.data.EL[i])
                    an.do_shift(point)
                    an.plot_beam(point)
                    if an.get_rssi_mac() > power:
                        power = an.get_rssi_mac()
                        best_point = point   
    return best_point
