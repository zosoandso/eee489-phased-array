import antenna_driver as an
import search
import time

while True:
    prompt = input('Enter antenna task: ')
    if prompt == '':
        break
    elif prompt == 'search':
        start = time.time()

        point = search.quick_search()
        print(f'initial look: {point}')
        point = search.search_nearby(point)
        print(f'narrowed search: {point}')

        print(f'run time: {time.time()-start}s')
    else:
        print('Invalid entry: try again.')
