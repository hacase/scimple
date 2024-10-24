import sys, time
from datetime import datetime as dt
from datetime import timedelta
import re
from urllib.request import urlopen
import json
from shutil import get_terminal_size


def sorter(l):
    return reversed(sorted(l, key=lambda x: x['real']))

def greening(string):
    this = '\033[38;5;34m' +string+ '\033[0;0m'
    return this


WINDOW_WIDTH = get_terminal_size((80, 20)).columns

URL_BASE = "https://swb-mobil.de/api/v1/stationboards/ass/"

URL_STIFT = "65251"
URL_LEDEN = "65249"
URL_ADEL = "65206"

URL_L = [URL_STIFT, URL_LEDEN, URL_ADEL]

URL_TIME = str(int(dt.now().timestamp() * 1000))
URL_END = "?v=" + URL_TIME + "&limit=30"

OFFSET = 2*60*60


while True:
    data = []

    for url_line in URL_L:
        webpage = urlopen(URL_BASE + url_line + URL_END, )
        html = webpage.read().decode("utf-8")
        hit = re.search("{.*}", html).group()

        jData = json.loads(hit)

        for i in jData['data'][:6]:
            page = {
                "line": i['line']['name'],
                "destination": i['headsign'],
                "eta": i['time'] + OFFSET,
                "real": i['realtime'] + OFFSET
            }

            data.append(page)

    for i_ride, ride in enumerate(sorter(data)):
        desti = ride['destination']
        if any(bonn in ride['destination'] for bonn in ['Bonn', 'Honnef', 'Hauptbahnhof']):
            destination_color = greening(desti)
        else:
            destination_color = desti

        if len(ride['line']) == 2:
            space = ' '
        else:
            space = ''

        print(ride['line'] +space+ ' -> ' + destination_color)

        seconds_day = 24*60*60
        string = ''
        string += str(timedelta(seconds=ride['eta'] % seconds_day)).rsplit(':', 1)[0]
        string += ', '
        string += str(timedelta(seconds=ride['real'] % seconds_day))

        arrival = timedelta(seconds=(ride['real'] - int(dt.now().timestamp()) - OFFSET) % seconds_day)
        print(string + f' => ETA: {round(arrival.total_seconds() / 60., 2)}min\n')


    print('\n' + '='*WINDOW_WIDTH  + '\n')
    time.sleep(30)
