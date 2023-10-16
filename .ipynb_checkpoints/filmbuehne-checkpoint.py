from urllib.request import urlopen
from urllib.parse import unquote
import re
import json
from datetime import datetime as dt

exclude = ['category', 'code']

def filmbuehne():
    timestamp = []
    title = []
    room = []
    runtime = []
    spec = []
    location = []
    ticket = []

    url = "https://www.kinoheld.de/ajax/getShowsForCinemas?cinemaIds%5B%5D=996&lang=de"
    page = urlopen(url)
    html = page.read().decode("utf-8")

    jstring = json.loads(html)

    for show in jstring['shows']:
        jtime = show['date'] +'-'+ show['time']
        timestamp.append(dt.strptime(jtime, '%Y-%m-%d-%H:%M'))
        title.append(show['name'])
        room.append(None)
        location.append('Filmbühne')
        runtime.append(show['duration'])

        jspec = ''
        for flags in show['flags']:
            for flag in flags:
                if flag not in exclude:
                    jspec += flags[flag] + '\n'
        if jspec[-1:] == '\n':
            jspec = jspec[:-1]
        spec.append(jspec)

        before = 'https://www.kinoheld.de/kino/bonn/neue-filmbuehne-bonn/vorstellung/'
        after = '?mode=widget&layout=movies&rb=0&hideFilters=1#panel-seats'
        ticket.append(before + show['id'] + after)
        
    result = {
        "timestamp": timestamp,
        "title": title,
        "room": room,
        "runtime": runtime,
        "spec": spec,
        "location": location,
        "ticket": ticket
    }
    
    return result