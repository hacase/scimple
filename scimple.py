import sys, time, random
import emoji
from datetime import datetime as dt
from datetime import timedelta
from shutil import get_terminal_size
import scimple_functions as SF

def slow_type(t):
    typing_speed = 375
    for l in t:
        sys.stdout.write(l)
        sys.stdout.flush()
        time.sleep(10.0/typing_speed)
    print('\n')

def opening():
    string = """     S how
     C inemas
     I n
     M y
     P lace
     L isting
     E verything"""

    print('')
    slow_type(string)
    
opening()

def inputexit(var):
    var = input(var)
    if var == 'exit':
        print('exited session.')
        sys.exit()
    else:
        return var


print(emoji.emojize(":T-Rex:"), 'Rex', emoji.emojize(":T-Rex:"))
print(emoji.emojize(":popcorn:"), 'WOKI', emoji.emojize(":popcorn:"))
print(emoji.emojize(":burrito:"), 'KINOPOLIS', emoji.emojize(":burrito:"))
print(emoji.emojize(":bread:"), 'Brotfabrik', emoji.emojize(":bread:"))
print(emoji.emojize(":NEW_button:"), 'Neue Filmbühne', emoji.emojize(":NEW_button:"))
print(emoji.emojize(":glowing_star:"), 'STERNLICHTSPIELE', emoji.emojize(":glowing_star:"))
print('')

imported = []

description = 'default is all, sort with -- [t]ime, [a]lphabet, [c]inema, [r]oom, [s]eat\n'

window_width = get_terminal_size((80, 20)).columns

if len(description) > window_width:
    for part in SF.breakline_space(description, window_width):
        print(part)
else:
    print(description)
    

def routine():
    sorter_key = None
    
    while True:
        is_date = False

        p_date = inputexit('date: ').lower().replace(' ', '')

        if '--' in p_date:
            p_date, sorter_key = p_date.split('--', 1)


        if str(p_date).lower() in [l.lower() for l in SF.l_today]:
            p_date = dt.today()

        elif str(p_date).lower() in [l.lower() for l in SF.l_tomorrow]:
            p_date = dt.today() + timedelta(days=1)

        elif str(p_date).lower() in [l.lower() for l in SF.l_dayname]:
            day_hit = SF.l_dayname.index(p_date.capitalize()) %7
            today = dt.today().strftime('')

            if day_hit < dt.today().weekday():
                day_skip = 7 - dt.today().weekday() + day_hit
            elif day_hit == dt.today().weekday():
                day_skip = 7
            else:
                day_skip = day_hit - dt.today().weekday()

            p_date = dt.today() + timedelta(days=day_skip)


        if p_date == '':
            p_date = 'all'
            is_date = True

        else:
            p_date, is_date = SF.detect_date(p_date)

        if is_date:
            break
        else:
            print('invalid date')


    if p_date == 'all':
        p_timestamp = False

    else:
        print('')
        while True:
            p_time = inputexit('time: ').lower().replace(' ', '')

            if p_time == '':
                p_time = '0000'

            if ':' in p_time:
                hour, minute = p_time.split(':', 1)
            else:
                hour = p_time[:-2]
                minute = p_time[-2:]

            try:
                p_timestamp = p_date.replace(hour=int(hour), minute=int(minute), second=0, microsecond=0)
                break

            except ValueError:
                print('invalid time')            

    print('')
    while True:
        p_cinema = inputexit('cinema: ').lower().replace(' ', '').split(',')

        if p_cinema == ['']:
            p_cinema = []
            for i in SF.cinema_alias:
                p_cinema.append(i[0])

        else:
            p_cinema = list(filter(None, p_cinema))

        p_cinema = list(set([SF.is_cinema_alias(p) for p in p_cinema]))

        if False in p_cinema:
            print('invalid cinema key.')
            continue

        else:
            for p in p_cinema:
                if not SF.cinema_in_dlist(p, imported):
                    desc = 'importing ' + p + '...'
                    end = p + ' done.'
                    loader = SF.Loader(desc, end).start()

                    imported.append(SF.import_cinema_errorless(p))

                    loader.stop()
            break    

    p_title = inputexit('\ntitle: ').lower().rstrip()
    if p_title == '':
        p_title = False
        
    print('')
    
    selected_cinema = [event for cinema in imported for selected in p_cinema if selected in cinema['alias'] for event in cinema['event']]
        
    SF.show(selected_cinema, sorter_key, p_timestamp, p_title)
    

while True:
    routine()
    print('\n\n\n\n')
