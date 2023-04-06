from typing import Tuple
import antenna as an

def dumb_search() -> None: # just a test demo don't use
    for i in range(0, len(an.data)):
        point =  (an.data.AZ[i], an.data.EL[i])
        an.do_shift(point)
        an.plot_beam(point)

def quick_search() -> Tuple[float, float]:
    power = []
    az = []
    el = []
    for i in range(0, len(an.data)):
        for angle in [0, 45, 90, 135, 180, 225, 270, 315]:
            if an.data.AZ[i] == angle:
                if an.data.EL[i] > 40 and an.data.EL[i] < 50:
                    point =  (an.data.AZ[i], an.data.EL[i])
                    an.do_shift(point)
                    an.plot_beam(point)
                    #power.append(an.get_rssi_linux())
                    power.append(an.get_rssi_mac())
                    az.append(point[0])
                    el.append(point[1])      
    max_index = power.index(max(power))
    return az[max_index], el[max_index]
