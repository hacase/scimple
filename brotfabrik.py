from urllib.request import urlopen
import re
from bs4 import BeautifulSoup
from datetime import datetime as dt

def brotfabrik():
    timestamp = []
    title = []
    room = []
    runtime = []
    spec = []
    location = []
    ticket = []

    url = "https://www.bonnerkinemathek.de/programm/"
    page = urlopen(url)
    html = page.read().decode("utf-8")

    pattern = r'<h2>.*?</a></div>'
    match_results = re.findall(pattern, html, re.DOTALL)


    for i in match_results:    
        soup = BeautifulSoup(i, "html.parser")

        for i in range(100):
            try:
                date = re.sub("<.*?>", "", str(soup.find("h2"))).split(' ', 1)[1]

                title.append(re.sub("<.*?>", "", soup.find_all("div", class_="title")[i].text))            
                spec.append(re.sub("<.*?>", "", soup.find_all("span", class_="spec")[i].text))
                time = re.sub("<.*?>", "", soup.find_all("span", class_="date")[i].text)
                location.append(re.sub("<.*?>", "", soup.find_all("div", class_="location")[i].text))
                ticket.append(re.sub("<.*?>", "", soup.find_all("a", class_="movie block-1", href=True)[i]['href']))
                room.append(None)
                runtime.append(None)

                timestamp.append(dt.strptime(date + time, '%d/%m/%Y%H:%M'))
            except:
                break


    result = {
        "timestamp": timestamp,
        "title": title,
        "room": location,
        "runtime": runtime,
        "spec": spec,
        "location": location,
        "ticket": ticket
    }
    
    return result