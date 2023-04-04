import antenna as ant

def dumb_search():
    for i in range(0, len(ant.data)):
        point = (ant.data.AZ[i], ant.data.EL[i])
        ant.do_shift(ant.get_angles(point))
