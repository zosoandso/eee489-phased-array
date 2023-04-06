import search

while True:
    prompt = input('Enter antenna task: ')
    if prompt == '':
        break
    elif prompt == 'search':
        initial_point = search.quick_search()
        search.point_and_show(initial_point)
    else:
        print('Invalid entry: try again.')
