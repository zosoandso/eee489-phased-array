import antenna as an
import search
import time

while True:
    prompt = input('Enter antenna task: ')
    if prompt == '':
        break
    elif prompt == 'search':
        start = time.time()

        point = search.quick_search()
        an.plot_beam(point)
        print(f'initial look: {point}')

        point = search.search_nearby(point)
        an.plot_beam(point)
        print(f'narrowed search: {point}')

        an.do_shift(point)

        print(f'run time: {time.time()-start}s')
    else:
        print('Invalid entry: try again.')
