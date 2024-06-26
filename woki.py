from urllib.request import urlopen
from urllib.parse import unquote
import re
import json
from datetime import datetime as dt

def notemptystring(value):
    if isinstance(value, str) and (value):
        return True
    else:
        return False


exclude = ['termine', 'vorstellungen_fakten', 'idf', 'filmreihe_id', 'plakat_ids',
           'manufotos', 'director', 'fsk', 'FSKdeskriptoren',
           'inhalt', 'plakat_subtext', 'KinoStart_hier', 'KinoStart_D',
           'filmreihe_name', 'filmnacht', 'vortext', 'fbw',
           'Kids', 'Kids', 'Kaffee', 'Sekt', 'Horror', 'Romance',
           'Action', 'Marvel', 'StarWars', 'Bond', 'Family', 'Live', 'Comedy',
           'Crime', 'Natur', 'Abenteuer', 'Sport', 'Fantasy', 'Krimi', 'Thriller',
           'Arthouse', 'Bier', 'Biography', 'History', 'Mystery', 'Musik',
           'Animation', 'Drama', 'ScienceFiction', 'Krieg', 'Headphones', 'StarTrek', 
           'Disney', 'Pixar', 'DC_Comics', 'Oscar', 'Doku',
           'titel', '2D', 'klon_von']

def woki():
    result = {
        "alias": ['woki', 'wk'],
        "event": []
    }

    url = "https://www.woki.de/programm"
    html = urlopen(url).read().decode("utf-8")

    pattern = r'<script> var programm .*?</script>'
    match_results = re.findall(pattern, html, re.DOTALL)

    match_results = ''.join(match_results).split('= ', 1)[1].rsplit('}', 1)[0] + '}'
    jstring = json.loads(match_results)

    for film in jstring["filme"]:
        l_vorstellung = []
        l_termine = []

        filmfakt = jstring["filme"][film]['filmfakten']
        jtitle = filmfakt['titel']

        jspec = ''
        for fakt in filmfakt:
            if notemptystring(filmfakt[fakt]) and fakt not in exclude:
                if filmfakt[fakt] == '1':
                    jspec += fakt + '\n'
                elif filmfakt[fakt] not in exclude:
                    if fakt == 'laufzeit':
                        jruntime = filmfakt[fakt]
                    else:
                        jspec += filmfakt[fakt] + '\n'

        try:
            l_vorstellung.append(jstring["filme"][film]['vorstellungen']['vorstellungen_fakten'])
            l_termine.append(jstring["filme"][film]['vorstellungen']['termine'])
        except TypeError:     
            for i in jstring["filme"][film]['vorstellungen']:
                l_vorstellung.append(i['vorstellungen_fakten'])
                l_termine.append(i['termine'])

        for vorstellung, termin in zip(l_vorstellung, l_termine):
            for fakt in vorstellung:
                if notemptystring(vorstellung[fakt]) and fakt not in exclude:
                    if vorstellung[fakt] not in jspec and fakt not in jspec:
                        if vorstellung[fakt] == '1':
                            jspec += fakt + '\n'
                        elif vorstellung[fakt] not in exclude:
                            jspec += vorstellung[fakt] + '\n'

            if all(val in jspec for val in ['2D', 'DreiD']):
                jspec = jspec.replace('2D\n', '')

            for day in termin:        
                if isinstance(termin[day], dict):
                    times = 1
                    termin[day] = [termin[day]]
                else:
                    times = len(termin[day])

                screen = termin[day]
                for i in range(times):
                    title = jtitle
                    if jspec[-2:-1] == '\n':
                        jspec = jspec[:-1]
                    spec = jspec[:-1].replace('\n', ' ')
                    
                    timestamp = dt.strptime(screen[i]['datum'] +'-'+ screen[i]['zeit'], '%Y-%m-%d-%H:%M')
                    room = screen[i]['saal']
                    runtime = jruntime
                    ticket = unquote(unquote(screen[i]['link_mobile']))
                

                    page = {
                        "name": 'WOKI',
                        "short name": 'woki',
                        "emoji": ':popcorn:',
                        "timestamp": timestamp,
                        "title": title,
                        "subtitle": None,
                        "room": room,
                        "seat": None,
                        "runtime": runtime,
                        "spec": spec,
                        "location": 'WOKI',
                        "ticket": ticket,
                        "load": None,
                        "price": None
                    }

                    result['event'].append(page)
    
    return result