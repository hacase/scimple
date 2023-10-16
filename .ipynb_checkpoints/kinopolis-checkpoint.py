from urllib.request import urlopen
from urllib.parse import unquote
import re
from bs4 import BeautifulSoup
from datetime import datetime as dt


def kinopolis():
    timestamp = []
    title = []
    room = []
    spec = []
    location = []
    ticket = []

    url = "https://www.kinopolis.de/bn/programm/woche-1"
    page = urlopen(url)
    html = page.read().decode("utf-8")

    pattern = r'<section class="bg.*?</section>'
    match_results = re.findall(pattern, html, re.DOTALL)

    for section in match_results[:-1]:        
        program = BeautifulSoup(section, "html.parser")   

        pattern = r'<h2 class="hl--1 hidden-max-xs">.*?</h2>'
        version = re.findall(pattern, str(program), re.DOTALL)
        _, _, name, rest = str(version).split('>', 3)
        jtitle, _ = name.split('<', 1)
    #    _, rest = rest.split('>', 1)
    #    if len(rest) > 2:
    #        jtitle2, _ = rest.split('<', 1)

        pattern = r"datetime.*?</time>"
        jtime = re.findall(pattern, section, re.DOTALL)
        i = 0    

        #print(program.prettify())    
        for prog in program.find_all("div", {"class": "prog"}):        
            for day in prog.find_all("a", {"class": "prog__day"}):
                day = str(day)

                #if jtitle2:
                #    title.append(jtitle, jtitle2)
                #else:
                #    title.append(jtitle)

                title.append(jtitle)

                pattern = r"data-version='.*?'"
                jspec = ','.join(re.findall(pattern, day, re.DOTALL))
                jspec = jspec.replace('data-version=', '').replace('"', '')
                jspec = jspec.replace('[', '').replace("'", '').replace("]", '')


                pattern = r'href=".*?"'
                ticket.append('https://www.kinopolis.de' + re.findall(pattern, day, re.DOTALL)[0][6:-1])

                label = [r'prog__label.*?</div>',
                        r'prog__time.*?</div>',
                        r'prog__version.*?</div>',
                        r'prog__extras.*?</div>',
                        r'prog__cinema.*?</div>']

                for pattern in label:
                    _, label = re.findall(pattern, day, re.DOTALL)[0].split('>', 1)
                    label, _ = label.split('<', 1)
                    if 'time' in pattern:
                        timestamp.append(dt.strptime(jtime[i][10:-21] +'.'+ label, '%Y-%m-%d.%H:%M')) 
                    elif 'cinema' in pattern:
                        room.append(label.replace('Kino', '').replace(' ', ''))
                    elif label:
                        jspec += ', ' + label

                spec.append(jspec)                    
                location.append('KINOPOLIS')

            i += 1

    result = {
        "timestamp": timestamp,
        "title": title,
        "room": room,
        "spec": spec,
        "location": location,
        "ticket": ticket
    }
    
    return result