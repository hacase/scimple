from urllib.request import urlopen
from urllib.parse import unquote
import re
import json
from datetime import datetime as dt

exclude = ['category', 'code']

def filmbuehne():
    result = {
        "alias": ['filmbuehne', 'fb', 'neue filmbuehne', 'filmbühne', 'neue filmbühne'],
        "event": []
    }

    url = "https://www.kinoheld.de/ajax/getShowsForCinemas?cinemaIds%5B%5D=996&lang=de"
    page = urlopen(url)
    html = page.read().decode("utf-8")

    jstring = json.loads(html)

    for show in jstring['shows']:
        jtime = show['date'] +'-'+ show['time']
        timestamp = dt.strptime(jtime, '%Y-%m-%d-%H:%M')
        title = show['name']
        runtime = show['duration']

        jspec = ''
        for flags in show['flags']:
            for flag in flags:
                if flag not in exclude:
                    jspec += flags[flag] + '\n'
        if jspec[-1:] == '\n':
            jspec = jspec[:-1]
        spec = jspec.replace('\n', ' ')

        before = 'https://www.kinoheld.de/kino/bonn/neue-filmbuehne-bonn/vorstellung/'
        after = '?mode=widget&layout=movies&rb=0&hideFilters=1#panel-seats'
        ticket = before + show['id'] + after
        
        page = {
            "name": 'Neue Filmbühne',
            "short name": 'filmbuehne',
            "emoji": ':NEW_button:',
            "timestamp": timestamp,
            "title": title,
            "subtitle": None,
            "room": None,
            "seat": None,
            "runtime": runtime,
            "spec": spec,
            "location": 'Neue Filmbühne',
            "ticket": ticket,
            "load": None,
            "price": None
        }
        
        result['event'].append(page)
    
    return result