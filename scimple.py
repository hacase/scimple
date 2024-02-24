import sys, time, random
from imdb import Cinemagoer
import rottentomatoes as rt
import requests
import emoji
from datetime import datetime as dt
from datetime import timedelta

string = """     Show
     Cinemas
     In
     My
     Place
     Listing
     Everything"""

typing_speed = 100 #wpm

def slow_type(t):
    for l in t:
        sys.stdout.write(l)
        sys.stdout.flush()
        time.sleep(random.random()*10.0/typing_speed)
    print('')

slow_type(string)

def inputexit(var):
    var = input(var)
    if var == 'exit':
        print('exited session.')
        sys.exit()
    else:
        return var
    
woki_alias = ['woki', 'wk']
brot_alias = ['brotfabrik', 'bf', 'brot']
rex_alias = ['rex', 'rx']
filmbuehne_alias = ['filmbuehne', 'fb', 'neue filmbuehne', 'filmbühne', 'neue filmbühne']

cinema_alias = [woki_alias, brot_alias, rex_alias, filmbuehne_alias]

l_today = ['t', 'today', 'h', 'heute']
l_tomorrow = ['tomorrow', 'm', 'morgen']
l_dayname = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday',
             'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun',
             'Montag', 'Dienstag', 'Mittwoch', 'Donnerstag', 'Freitag', 'Samstag', 'Sonntag',
             'Mo', 'Di', 'Mi', 'Do', 'Fr', 'Sa', 'So']
    
def detect_date(date, return_bool=False):
    day = None
    month = None
    year = None
    
    if date[-1] == '.':
        date = date[:-1]
    
    if date.count('.') == 1:
        first, second = date.split('.')
        
        if int(second) > 12:
            if int(second) > 1900:
                year = '20' + second
            else:
                year = second
            month = first
            
        else:
            day = first
            month = second
            
    elif date.count('.') == 2:
        first, second, third = date.split('.')
        day = first
        month = second
        if int(third) > 1900:
            year = third
        else:
            year = '20' + third
    
    else:
        day = date
        
    date = ''
    key = ''

    if day:
        date += day +'.'
        key += '%d.'

    if month:
        date += month +'.'
        key += '%m.'

    if year:
        date += year
        key += '%Y'

    try:
        if return_bool:
            return True
        else:
            return dt.strptime(date, key)
        
    except ValueError:
        return False        

def breakline_space(text, width):
    firstinline = True
    lines = []
    l = ''
    
    for t in text.split(' '):
        if len(t) > width:
            firstinline = True
            
            if l:
                initial = width - len(l) - 1
                lines.append(l +' '+ t[:initial])
            else:
                initial = 0
                            
            for part in [t[initial +i:initial +i +width] for i in range(1, len(t)-initial, width)]:
                lines.append(part)
            
            if len(lines[-1]) != width:
                l = lines.pop()
            else:
                l = ''
            
        else:
            if len(l) +1 +len(t) > width:
                lines.append(l)
                l = ''
                firstinline = True

            if firstinline:
                if len(l + t) +1 >= width:
                    lines.append(t)
                    l = ''
                    firstinline = True
                else:
                    l += t
                    firstinline = False
            else:
                l += ' ' + t
                
    if l:
        lines.append(l)
        
    return lines
        
def show_event(event_d):
    window_width = 48
    print(emoji.emojize(event_d['emoji']), event_d['title'])
    print('-'*window_width)
    
    if event_d['runtime']:
        string = event_d['timestamp'].strftime('%d.%m %a, %H:%M, ') + f"{event_d['runtime']}min"
    else:
        string = event_d['timestamp'].strftime('%d.%m %a, %H:%M')

    if event_d['room']:
        string += f", Saal: {event_d['room']}"
    
    print(string)
    
    comment = event_d['location']
    if event_d['spec']:
        comment += ' ' + event_d['spec']
    
    if len(comment) > window_width:
        for part in breakline_space(comment, window_width):
            print(part)
    else:
        print(comment)
            
    print(event_d['ticket'], '\n')
    
def import_all():
    import woki as wk
    import brotfabrik as bf
    import rex as rx
    import filmbuehne as fb
    
    woki = wk.woki()
    brot = bf.brotfabrik()
    rex = rx.rex()
    buehne = fb.filmbuehne()
    
    return (woki, brot, rex, buehne)

def import_cinema(name):
    if name in woki_alias:
        import woki as wk
        return wk.woki()
    
    elif name in brot_alias:
        import brotfabrik as brot
        return bf.brotfabrik()
    
    elif name in rex_alias:
        import rex as rx
        return rx.rex()
        
    elif name in filmbuehne_alias:
        import filmbuehne as fb
        return fb.filmbuehne()
        
    else:
        return False
    
def check_import(package):
    if package in sys.modules:
        return True  
    else:
        return False

def show_date(timestamp, l_cinema):
    for cinema in l_cinema:
        for event in cinema['event']:
            if event['timestamp'].strftime('%d.%m') == timestamp.strftime('%d.%m'):
                show_event(event)
                
def dict_dublicate(c, l):
    for i in l:
        if (type(i) == dict and int):
            return 'this'
            
def is_cinema_alias(var):
    for i in cinema_alias:
        if var in i:
            result = i[0]
        else:
            result = False
            
    return result

def multicinema(var):
    result = []
    
    if ',,' in var:
        for c in var.split(',,'):
            tmp = is_cinema_alias(c)
            if tmp:
                result.append(tmp)
    
    return result if len(result) != 0 else [var]

def get_from_alias(name):
    result = False
    for c in cinema_alias:
        if name in c:
            result = c[0]
    
    return result        
                

print('\n')

print(emoji.emojize(":popcorn:"), 'WOKI', emoji.emojize(":popcorn:"))

print(emoji.emojize(":bread:"), 'Brotfabrik', emoji.emojize(":bread:"))

print(emoji.emojize(":T-Rex:"), 'Rex', emoji.emojize(":T-Rex:"))

print(emoji.emojize(":NEW_button:"), 'Neue Filmbühne', emoji.emojize(":NEW_button:"))

print('\n')

l_cinema = []  

while True:
    prompt = inputexit('prompt: ').lower()

    if ' ' in prompt:
        var, var_cinema = prompt.split(' ', 1)
        
        l_cinema = multicinema(var_cinema)

        for cinema in l_cinema:
            cinema = get_from_alias(cinema)

            if type(cinema) != dict:
                l_cinema[l_cinema.index(cinema)] = import_cinema(cinema)

            if cinema == False:
                print('This cinema', var_cinema[l_cinema.index(cinema)], 'is unknown.')

    else:
        var = prompt
        l_cinema = import_all()


    l_cinema = [i for i in l_cinema if i]


    if any(var in l for l in l_today):
        print('')
        show_date(dt.today(), l_cinema)

    elif any(var in l for l in l_tomorrow):
        print('')
        show_date(dt.today() + timedelta(days=1), l_cinema)

    elif any(var.lower() in l.lower() for l in l_dayname):
        day_hit = l_dayname.index(var.capitalize())%7
        today = dt.today().strftime('')

        if day_hit < dt.today().weekday():
            day_skip = 7 - dt.today().weekday() + day_hit
        elif day_hit == dt.today().weekday():
            day_skip = 7
        else:
            day_skip = day_hit - dt.today().weekday()

        show_date(dt.today() + timedelta(days = day_skip), l_cinema)

    elif detect_date(var):
        show_date(dt.today(), l_cinema)