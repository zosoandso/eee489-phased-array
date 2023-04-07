import antenna_driver as an
import search

while True:
    prompt = input('Enter antenna task: ')
    if prompt == '':
        break
    elif prompt == 'search':
        point = search.quick_search()
        point = search.search_nearby(point)
    else:
        print('Invalid entry: try again.')
