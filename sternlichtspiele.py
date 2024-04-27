from urllib.request import urlopen
import json
from datetime import datetime as dt


def sternlichtspiele():
    result = {
        "alias": ['sternlichtspiele', 'sl', 'stern', 'sternkino'],
        "event": []
    }
    
    url = "https://www.cinestar.de/api/cinema/11/show/"
    html = urlopen(url).read().decode("utf-8")
    
    for i in json.loads(html):
        title = i['title']
        
        subtitle = i['subtitle']
        
        showtimes = i['showtimes']
    
        for j in showtimes:
            timestamp = dt.strptime(j['datetime'].replace(' UTC', ''), '%Y-%m-%d %H:%M')
            
            attributes = j['attributes']
            
            if subtitle:
                spec = subtitle +','+ ', '.join(attributes)
            else:
                spec = ', '.join(attributes)
            
            pre_link = 'https://webticketing3.cinestar.de/?cinemaId=32374&movieSessionId='
            systemID = j['systemId']
            ticket = pre_link + systemID
    
            l_screen = [51, None, 53]
            l_seat = ['212', '70+1', '233+4']
            screen = j['screen']
            room = l_screen.index(screen) + 1
            seat = l_seat[l_screen.index(screen)]

            page = {
                "name": 'STERNLICHTSPIELE',
                "short name": 'stern',
                "emoji": ':glowing_star:',
                "timestamp": timestamp,
                "title": title,
                "subtitle": None,
                "room": room,
                "seat": seat,
                "runtime": None,
                "spec": spec,
                "location": 'STERNLICHTSPIELE',
                "ticket": ticket,
                "load": None,
                "price": None
            }
        
            result['event'].append(page)
    
    return result