from urllib.request import urlopen
import re
import json
from datetime import datetime as dt


def capitol_siegburg():
    result = {
        "alias": ['Capitol Kinocenter', 'cs', 'capitol', 'capitol siegburg'],
        "event": []
    }

    url = "https://www.capitol-siegburg.de/programm"
    html = urlopen(url).read().decode("utf-8")
    
    ignore_value = ['{}', '', 'idf']
    
    pattern = r'var programm = .*?; var wallpaper'
    sub_match_results = re.search(pattern, html, re.DOTALL)[0][15:-15]
    match_results = json.loads(sub_match_results)['filme']
    
    for _, film in match_results.items():
        film_fakten = film['filmfakten']
        
        l_spec = []
        l_spec.append(film_fakten['Versionsmarker'])
    
        title = film_fakten['titel']
    
        runtime = film_fakten['laufzeit']
    
        vorst_fakten = film['vorstellungen']
    
        for key, value in vorst_fakten['vorstellungen_fakten'].items():
            if str(value) not in ignore_value and key not in ignore_value:
                if value == '1':
                    l_spec.append(key.capitalize())
                else:
                    l_spec.append(str(key) +': '+ str(value))
    
        for _, info in vorst_fakten['termine'].items():
            if isinstance(info, dict):
                info = [info]
    
            for termin in info:
                time = termin['datum'] +'-'+ termin['zeit']
                timestamp = dt.strptime(time, '%Y-%m-%d-%H:%M')
    
                room = termin['saal']
    
                ticket = termin['link_desktop']
    
                spec = ', '.join(l_spec)
    
    
                page = {
                    "name": 'Capitol Kinocenter',
                    "short name": 'capitol',
                    "emoji": ':film_frames:',
                    "timestamp": timestamp,
                    "title": title,
                    "subtitle": None,
                    "room": room,
                    "seat": None,
                    "runtime": runtime,
                    "spec": spec,
                    "location": 'Capitol Kinocenter',
                    "ticket": ticket,
                    "load": None,
                    "price": None
                }
    
                result['event'].append(page)

    return result