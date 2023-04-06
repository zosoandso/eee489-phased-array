import antenna as an
import search

while True:
    prompt = input('Enter antenna task: ')
    if prompt == '':
        break
    elif prompt == 'search':
        initial_point = search.quick_search()
        an.do_shift(initial_point)
        an.plot_beam(initial_point)
    else:
        print('Invalid entry: try again.')
