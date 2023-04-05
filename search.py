import antenna as ant

data = ant.pd.read_csv('points.csv')

def dumb_search() -> None: # don't use this it's uselessly slow
    for i in range(0, len(ant.data)):
        point = (ant.data.AZ[i], ant.data.EL[i])
        ant.do_shift(ant.get_command(point))
        ant.plot_beam(point)

def quick_search() -> None:
    for i in range(0, len(data)):
        point = (data.az[i], data.el[i])
        ant.do_shift(ant.get_command(point))
        ant.plot_beam(point)
