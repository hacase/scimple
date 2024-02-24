from urllib.request import urlopen
from urllib.parse import unquote
import re
import json
from datetime import datetime as dt

exclude = ['category', 'code']

def rex():
    result = {
        "alias": ['rex', 'rx'],
        "event": []}

    url = "https://www.kinoheld.de/ajax/getShowsForCinemas?cinemaIds%5B%5D=1093&lang=de"
    page = urlopen(url)
    html = page.read().decode("utf-8")

    jstring = json.loads(html)

    for show in jstring['shows']:
        jtime = show['date'] +'-'+ show['time']
        timestamp = dt.strptime(jtime, '%Y-%m-%d-%H:%M')
        title = show['name']
        room = None
        location = 'REX'
        runtime = show['duration']

        jspec = ''
        for flags in show['flags']:
            for flag in flags:
                if flag not in exclude:
                    jspec += flags[flag] + '\n'
        if jspec[-1:] == '\n':
            jspec = jspec[:-1]
        spec = jspec.replace('\n', ' ')

        before = 'https://www.kinoheld.de/kino/bonn/rex-lichtspieltheater-bonn/vorstellung/'
        after = '?mode=widget&layout=movies&rb=0&hideFilters=1#panel-seats'
        ticket = before + show['id'] + after
    
        page = {
            "name": 'REX',
            "short name": 'rex',
            "emoji": ':T-Rex:',
            "timestamp": timestamp,
            "title": title,
            "room": room,
            "runtime": runtime,
            "spec": spec,
            "location": location,
            "ticket": ticket
        }
        
        result['event'].append(page)
    
    return result