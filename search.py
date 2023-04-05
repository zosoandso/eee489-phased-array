import antenna as an

def dumb_search() -> None: # don't use this it's uselessly slow
    for i in range(0, len(an.data)):
        point =  (an.data.AZ[i], an.data.EL[i])
        an.do_shift(point)
        an.plot_beam(point)

def quick_search() -> None:
    power = []
    for i in range(0, len(an.data)):
        for angle in [0, 45, 90, 135, 180, 225, 270, 315]:
            if an.data.AZ[i] == angle:
                if an.data.EL[i] > 40 and an.data.EL[i] < 50:
                    point =  (an.data.AZ[i], an.data.EL[i])
                    an.do_shift(point)
                    an.plot_beam(point)
                    power.append(an.get_rssi_mac())
    print(f'Best RSSI: {max(power)}')
    print(f'Azimuth: {an.data.AZ[power.index(max(power))]}')
    print(f'Elevation: {an.data.EL[power.index(max(power))]}')
