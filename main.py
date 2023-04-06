import antenna as an
import search

while True:
    prompt = input('Enter antenna task: ')
    if prompt == '':
        break
    elif prompt == 'search':
        point = search.quick_search()
        print(point)
        point = search.search_nearby_az(point)
        an.do_shift(point)
        an.plot_beam(point)
    else:
        print('Invalid entry: try again.')
