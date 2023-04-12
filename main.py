import antenna_driver as an
import search
import Step_Track

while True:
    prompt = input('Enter antenna task (help for list of commands): ')
    if prompt == 'help':
        print('connect: connects to specifed access point (AP)')
        print('search: directs antenna to point at static AP')
        print('track: tracks relative movement of AP and adjusts antenna')
        print('exit: leaves the antenna control environment')
    if prompt == 'exit':
        break
    elif prompt == 'connect':
        an.connect()
    elif prompt == 'search':
        point = search.quick_search()
        search.search_nearby(point)
    elif prompt == 'track':
        print()
    else:
        print('Invalid entry try again.')
