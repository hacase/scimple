import sys, time
import requests
import emoji
from datetime import datetime as dt
from datetime import timedelta
from itertools import cycle
from shutil import get_terminal_size
from threading import Thread
from pyparsing import *


woki_alias = ['woki', 'wk']
brot_alias = ['brotfabrik', 'bf', 'brot']
rex_alias = ['rex', 'rx']
filmbuehne_alias = ['filmbuehne', 'fb', 'neue filmbuehne', 'filmbühne', 'neue filmbühne']
kinopolis_alias = ['kinopolis', 'kp']

cinema_alias = [woki_alias,
                brot_alias,
                rex_alias,
                filmbuehne_alias,
                kinopolis_alias]

l_today = ['t', 'today', 'h', 'heute']
l_tomorrow = ['tomorrow', 'm', 'morgen']
l_dayname = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday',
             'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun',
             'Montag', 'Dienstag', 'Mittwoch', 'Donnerstag', 'Freitag', 'Samstag', 'Sonntag',
             'Mo', 'Di', 'Mi', 'Do', 'Fr', 'Sa', 'So']

l_daybuzz = l_today + l_tomorrow + l_dayname

        
def detect_date(date):
    if type(date) == type(dt.now()):
        return (date, True)
    
    try:
        day = None
        month = None
        year = None

        if date[-1] == '.':
            date = date[:-1]

        if date.count('.') == 1:
            first, second = date.split('.')

            if int(second) > 12:
                if int(second) < 1900:
                    year = '20' + second
                else:
                    year = second
                month = first

            else:
                day = first
                month = second
                year = str(dt.today().year)

        elif date.count('.') == 2:
            first, second, third = date.split('.')
            day = first
            month = second
            if int(third) < 1900:
                year = '20' + third
            else:
                year = third

        else:
            day = date
            month = str(dt.now().month)
            year = str(dt.now().year)

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
            
            
    except TypeError:
        return (False, False)

    try:
        return (dt.strptime(date, key), True)
        
    except ValueError:
        return (False, False)  
    
def cinema_in_dlist(cinema, dlist):
    result = False
    
    if not dlist:
        return result
    else:
        for d in dlist:
            if cinema in d['alias']:
                result = True
                return result
            
def is_cinema_alias(var):
    for i in cinema_alias:
        if var in i:
            result = i[0]
            break
        else:
            result = False
            
    return result

def import_cinema(name):
    if name in woki_alias:
        import woki
        return woki.woki()
    
    elif name in brot_alias:
        import brotfabrik
        return brotfabrik.brotfabrik()
    
    elif name in rex_alias:
        import rex
        return rex.rex()
        
    elif name in filmbuehne_alias:
        import filmbuehne
        return filmbuehne.filmbuehne()
    
    elif name in kinopolis_alias:
        import kinopolis
        return kinopolis.kinopolis()
        
    else:
        return False
    
def import_cinema_errorless(name):
    while True:
        try:
            result = import_cinema(name)

        except Exception as e:
            print("\r" , end="", flush=True)
            
            print(e)
            time.sleep(4)
        else:
            return result
        
class Loader:
    def __init__(self, desc="Loading...", end="Done!", timeout=0.1):
        """
        A loader-like context manager

        Args:
            desc (str, optional): The loader's description. Defaults to "Loading...".
            end (str, optional): Final print. Defaults to "Done!".
            timeout (float, optional): Sleep time between prints. Defaults to 0.1.
        """
        self.desc = desc
        self.end = end
        self.timeout = timeout

        self._thread = Thread(target=self._animate, daemon=True)
        self.steps = ["⢿", "⣻", "⣽", "⣾", "⣷", "⣯", "⣟", "⡿"]
        self.done = False

    def start(self):
        self._thread.start()
        return self

    def _animate(self):
        for c in cycle(self.steps):
            if self.done:
                break
            print(f"\r{self.desc} {c}", flush=True, end="")
            time.sleep(self.timeout)

    def __enter__(self):
        self.start()

    def stop(self):
        self.done = True
        cols = get_terminal_size((80, 20)).columns
        print("\r" + " " * cols, end="", flush=True)
        print(f"\r{self.end}", flush=True)

    def __exit__(self, exc_type, exc_value, tb):
        # handle exceptions with those variables ^
        self.stop()


    
def return_color(string, color):
    this = '\033[38;5;'+ color +'m' + string +'\033[0;0m'
    return this

def color_len(line):
    ESC = Literal('\033')
    integer = Word(nums)
    escapeSeq = Combine(ESC + '[' + Optional(delimitedList(integer,';')) + oneOf(list(alphas)))

    nonAnsiString = lambda s : Suppress(escapeSeq).transformString(s)
    
    return len(nonAnsiString(line))

def breakline_space_col(text, width):
    firstinline = True
    lines = []
    l = ''
    
    for t in text.split(' '):
        if color_len(t) > width:
            firstinline = True
            
            if l:
                initial = width - color_len(l) - 1
                lines.append(l +' '+ t[:initial])
            else:
                initial = 0
                            
            for part in [t[initial +i:initial +i +width] for i in range(1, color_len(t)-initial, width)]:
                lines.append(part)
            
            if color_len(lines[-1]) != width:
                l = lines.pop()
            else:
                l = ''
            
        else:
            if color_len(l) +1 +color_len(t) > width:
                lines.append(l)
                l = ''
                firstinline = True

            if firstinline:
                if color_len(l + t) +1 >= width:
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
    window_width = 48#get_terminal_size((80, 20)).columns
    
    output_title = event_d['title']
    
    if event_d['subtitle']:
        output_title += ' / '+ event_d['subtitle']
        
    output_title = '@@' +' '+ output_title
    
    broken_title = ''
        
    if len(output_title) > window_width:
        for part in breakline_space(output_title, window_width):
            broken_title += part.replace('@@', emoji.emojize(event_d['emoji']), 1) + '\n'
    else:
        broken_title = output_title.replace('@@', emoji.emojize(event_d['emoji']), 1) + '\n'
        
    broken_title = broken_title[:-1]
    
    if event_d['timestamp'] > dt.now():
        event_colored = broken_title
    else:
        event_colored = return_color(broken_title, '160')
        
    print(event_colored)
        
    print('-'*window_width)
    
    if event_d['runtime']:
        string = event_d['timestamp'].strftime('%d.%m %a, %H:%M, ') + f"{event_d['runtime']}min"
    else:
        string = event_d['timestamp'].strftime('%d.%m %a, %H:%M')

    if event_d['room']:
        string += f", Saal: {event_d['room']}"
    
    if event_d['seat']:
        string += f", {event_d['seat']} seats"
        
    if event_d['load']:
        string += f", {event_d['load']}"
    
    if len(string) > window_width:
        for part in breakline_space(string, window_width):
            print(part)
    else:
        print(string)

    
    comment = event_d['location']
    
    if event_d['price']:
        comment += '; ' + event_d['price']
        
    l_highlight = ['ov', 'omu']
    
    if event_d['spec']:
        comment += '; ' + event_d['spec']
    
    splitted = comment.split(' ')
    for i in range(len(splitted)):
        if splitted[i].lower() in l_highlight:
            splitted[i] = return_color(splitted[i], '34')

        elif splitted[i][:-1].lower() in l_highlight and not splitted[i][-1].isalpha():
            splitted[i] = return_color(splitted[i][:-1], '34') + splitted[i][-1]

    comment = ' '.join(splitted)
        
    
    if color_len(comment) > window_width:
        for part in breakline_space_col(comment, window_width):
            print(part)
    else:
        print(comment)

    if event_d['ticket']:
        print(return_color(event_d['ticket'], '39'))
    else:
        print('--< no link >--')
    print('')
    
def sorter(d, sorter_key=None):
    try:
        if sorter_key == 'a':
            d = sorted(d, key=lambda l: l['title'])
            
        elif sorter_key == 't':
            d = sorted(d, key=lambda l: l['timestamp'])
            
        elif sorter_key == 'r':
            d = sorted(d, key=lambda l: (l['room'] is None, l['room']))
            
        elif sorter_key == 's':
            d = sorted(d, key=lambda l: (l['seat'] is None, l['seat']))
            
        elif sorter_key == 'c':
            d = sorted(d, key=lambda l: l['name'])
            
        else:
            d = sorted(d, key=lambda l: l['timestamp'])
            
    except TypeError:
        d = sorted(d, key=lambda l: l['timestamp'])
    
    return d

def valid_date(event, timestamp):
    result = False
    
    if timestamp == False:
        result = True
    
    elif event.strftime('%Y%m%d') == timestamp.strftime('%Y%m%d'):
        if event.strftime('%H%M') >= timestamp.strftime('%H%M'):
            result = True
            
    return result

def valid_title(event, title):
    result = False
    
    if title == False:
        result = True
    
    elif title.lower() in event.lower():
        result = True
            
    return result

def show(l_event, sorter_key, timestamp, title):
    flag = False
    
    for event in sorter(l_event, sorter_key):
        full_title = event['title']
        if event['subtitle']:
            full_title += ' ' + event['subtitle']
        
        if not (timestamp or title):
            flag = True
            show_event(event)    
        
        elif valid_date(event['timestamp'], timestamp) and valid_title(full_title, title):
            flag = True
            show_event(event)

    if not flag:
        print('\n-< no hits >-\n')