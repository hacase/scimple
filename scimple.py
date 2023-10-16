import sys, time, random
from imdb import Cinemagoer
import rottentomatoes as rt
import requests
import emoji

import woki as wk
import brotfabrik as bf
import rex as rx
import filmbuehne as fb

def abort(var):
    if var == 'exit':
        print('exited session.')
        sys.exit()
    else:
        return var

woki = wk.woki()
brot = bf.brotfabrik()
rex = rx.rex()
buehne = fb.filmbuehne()

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

print(emoji.emojize(":popcorn:"), 'WOKI', emoji.emojize(":popcorn:"))

print(emoji.emojize(":bread:"), 'Brotfabrik', emoji.emojize(":bread:"))

print(emoji.emojize(":T-Rex:"), 'Rex', emoji.emojize(":T-Rex:"))

print(emoji.emojize(":NEW_button:"), 'Neue Filmbühne', emoji.emojize(":NEW_button:"))

for i in range(len(brot['title'])):
    print(brot['title'][i])
    print(brot['timestamp'][i].strftime('%d.%m %a, %H:%M'))
    print(brot['room'][i])
    print(brot['runtime'][i])
    print(brot['spec'][i])
    print(brot['location'][i])
    print(f"\033[38;5;26m{brot['ticket'][i]}\x1b[0m")
    print('\n')