from urllib.request import urlopen
import re
from bs4 import BeautifulSoup
from datetime import datetime as dt

def brotfabrik():
    result = {
        "alias": ['brotfabrik', 'bf', 'brot'],
        "event": []}

    url = "https://www.bonnerkinemathek.de/programm/"
    page = urlopen(url, )
    html = page.read().decode("utf-8")

    pattern = r'<h2>.*?</a></div>'
    match_results = re.findall(pattern, html, re.DOTALL)


    for hit in match_results:    
        soup = BeautifulSoup(hit, "html.parser")

        for i in range(100):
            try:
                date = re.sub("<.*?>", "", str(soup.find("h2"))).split(' ', 1)[1]
                time = re.sub("<.*?>", "", soup.find_all("span", class_="date")[i].text)
                timestamp = dt.strptime(date + time, '%d/%m/%Y%H:%M')
                
                title = re.sub("<.*?>", "", soup.find_all("div", class_="title")[i].text)
                spec = re.sub("<.*?>", "", soup.find_all("span", class_="spec")[i].text).replace('\n', ' ')
                location = re.sub("<.*?>", "", soup.find_all("div", class_="location")[i].text)
                ticket = re.sub("<.*?>", "", soup.find_all("a", class_="movie block-1", href=True)[i]['href'])
                room = None
                runtime = None
                seat = None
                
                page = {
                    "name": 'Brotfabrik',
                    "short name": 'brotfabrik',
                    "emoji": ':bread:',
                    "timestamp": timestamp,
                    "title": title,
                    "room": room,
                    "seat": seat,
                    "runtime": runtime,
                    "spec": spec,
                    "location": location,
                    "ticket": ticket
                }

                result['event'].append(page)

            except:
                break
        
    return result