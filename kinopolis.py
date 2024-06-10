from urllib.request import urlopen
from urllib.parse import unquote
import re
import json
from datetime import datetime as dt
from datetime import timedelta
from bs4 import BeautifulSoup
import scimple_functions as SF

def None_AttributeError_cnt(function):
    try:
        return function.contents[0]
    except:
        return None

def kinopolis_week(url, url_week):
    result_event = []
    
    html = SF.open_url_errorless(url, url_week).read().decode("utf-8")
    
    soup = BeautifulSoup(html, "html.parser")
    match_results = soup.find_all("section", {"class": "bg-2 movie mb-2"})
    for program in match_results:
        title = program.find("a", {"class": "hl-link", "href": True}).contents[0]

        subtitle = program.find("span", {"class": "hl--sub"})
        if subtitle and len(subtitle.contents) > 0:
            subtitle = subtitle.contents[0]
        else:
            subtitle = None

        jspec = program.find_all("div", {"class": "movie__specs-el"})
        all_spec = []
        for i in jspec:
            if 'FSK' in str(i):
                all_spec.append(str(i).split('</span> ', 1)[1].split('<', 1)[0])

            elif 'Dauer' in str(i):
                runtime = str(i).split('</span> ', 1)[1].split('<', 1)[0].replace('Minuten', '').replace(' ', '')

        spec_caption = []
        caption_wrap = program.find_all("div", {"class": "caption__wrap"})
        if caption_wrap:
            for caption in caption_wrap:
                tmp = caption.find("b")
                if tmp:
                    caption_tag = tmp.contents[0]
                    caption_text = caption.find("div", {"class": "caption__text"}).contents[0].replace(' - Atmos', '')

                    for t in [title, subtitle]:
                        caption_text = "".join(caption_text.split(t)).lstrip().rstrip()

                    if caption_tag in caption_text:
                        caption_text = caption_text.split(caption_tag)[1].replace(':', '')

                    if [caption_tag, caption_text] not in spec_caption:
                        spec_caption.append([caption_tag, caption_text])

                else:
                    string = [c.string for c in caption if c.string not in [None, '\n']]
                    if len(string) == 1:
                        string = string[0]
                    else:
                        string = ': '.join([c.string for c in caption if c != '\n'])
                    spec_caption.append(['tag_all', string])


        l_day = []
        l_price = []

        table = program.find_all("div", {"class": "slider slider-6 prog-nav"})
        pattern = r'data-performance-ids=".*?</div></div></div>'
        for slider in re.findall(pattern, str(table)):        
            day = re.search('<div class="prog-nav__day">(.*?)</div>', slider).group(1)

            if 'Heute' in day:
                if dt.today().hour <= 1:
                    day = dt.today() + timedelta(-1)
                else:
                    day = dt.today()

            elif 'Morgen' in day:
                if dt.today().hour <= 1:
                    day = dt.today()
                else:
                    day = dt.today() + timedelta(+1)

            else:
                day = dt.strptime(day.split(' ')[-1], '%d.%m.')

            l_day.append(day.replace(year=dt.today().year, second=0, microsecond=0))


        i = -1
        for day_slide in program.find_all("div", {"class": "prog-day__wrapper"}):
            i += 1
            day = l_day[i]

            for screen in day_slide.find_all("div", {"class": "prog2__cont", "data-performance-id": True}):            
                time = None_AttributeError_cnt(screen.find("div", {"class": "prog2__time"}))
                if time:
                    hour, minute = time.split(':', 1)
                    timestamp = day.replace(hour=int(hour), minute=int(minute))

                else:
                    timestamp = None

                try:
                    room = re.search('<div>(.*?)</div>', str(screen)).group(1)
                except:
                    room = None

                seat = None_AttributeError_cnt(screen.find("div", {"class": "prog2__seats"}))

                load = None_AttributeError_cnt(screen.find("div", {"class": "prog2__scale scale-100"}))

                try:
                    tmp = screen.find("a", {"data-version": True, "href": True})['data-version'].replace('[', '').replace(']', '')
                    tmp = tmp.replace('"', '').upper().split(',')

                    if '2D' in tmp:
                        tmp.remove('2D')

                    if all(i in tmp for i in ['OV', 'OMU']):
                        tmp.remove('OV')

                    spec = []                
                    [spec.append(i) for i in tmp if i not in all_spec + spec]

                    for caption in spec_caption:
                        if caption[0] == 'tag_all':
                            all_spec.append(caption[1])

                        elif any(caption[0].lower() == t.lower() for t in spec):
                            spec = [caption[0] +': '+ caption[1] if s.lower() == caption[0].lower() else s for s in spec]

                    spec = ', '.join(all_spec + spec)
                except:
                    spec = ', '.join(all_spec)

                try:
                    ticket = 'https://www.kinopolis.de' + screen.find("a", {"data-version": True, "href": True})['href']
                except:
                    ticket = None

                price = None_AttributeError_cnt(screen.find("b"))
                if price:
                    price = price + '€'


                page = {
                    "name": 'KINOPOLIS',
                    "short name": 'kinopolis',
                    "emoji": ':burrito:',
                    "timestamp": timestamp,
                    "title": title,
                    "subtitle": subtitle,
                    "room": room,
                    "seat": seat,
                    "runtime": runtime,
                    "spec": spec,
                    "location": 'KINOPOLIS',
                    "ticket": ticket,
                    "load": load,
                    "price": price
                }

                result_event.append(page)
                
    return result_event

def kinopolis():
    result = {
        "alias": ['kinopolis', 'kp'],
        "event": []
    }
    
    raw_url = "https://www.kinopolis.de/bn/programm"
    
    for week in range(1, 8):
        url = raw_url + '/woche-' + str(week)

        for event in kinopolis_week(url, week):
            result['event'].append(event)
        
    return result
