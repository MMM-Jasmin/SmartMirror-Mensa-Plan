#!/usr/bin/python3
'''
update on vps:
    scp mensa_api.py ionos:/root/ubi-mensa/
    scp mensa_api.py mensa_tg.py ionos:/root/ubi-mensa/
'''
import csv
from lxml import html, etree
import requests
from datetime import datetime
import random
import pathlib
dir_path = pathlib.Path(__file__).parent.absolute()

url = 'https://www.studierendenwerk-bielefeld.de/essen-trinken/speiseplan/bielefeld/mensa-x/'

user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15'
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 13_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15'
]

def fetch_menu_dict():
    # set random user agent
    headers = {'User-Agent': random.choice(user_agents)}
    page = requests.get(url, headers=headers)
    tree = html.fromstring(page.text)

    datestr_today = datetime.now().strftime("%Y%m%d")
    menu_today = tree.find(f".//div[@id='menuContainer']/div[@class='menuTabs']/div[@data-selector='{datestr_today}']")
    if menu_today is None:
        return None
    
    menu_d = dict({"date": datestr_today, "mains":{}, "sides":{}})
    for menu in menu_today.xpath("div[contains(@class, 'menuItem--mainmenu')]//div[contains(@class, 'modal-body')]"):

        menu_name = menu.xpath(".//ul[li/*[text()[contains(.,'Hauptgerichte')]]]/li/strong/text()") # multiple menus per entry, "Aktiontheke" only?
        if len(menu_name) == 0:
            menu_name = menu.xpath(".//strong[contains(@class,'menuItem__headline')]/text()") # single menu per entry
        
        menu_type = menu.xpath(".//span[contains(@class,'menuItem__line')]/text()")[0].strip()
        menu_type = menu_type.replace("Mensa ","").title()

        menu_side = menu.xpath(".//ul[li/*[text()[contains(.,'Beilagen')]]]/li/strong/text()")

        # remove multiple spaces
        menu_name = [" ".join(n.split()) for n in menu_name] 
        menu_side = [" ".join(s.split()) for s in menu_side]

        menu_d["mains"][menu_type] = {"name": menu_name, 'side': menu_side}
    if len(menu_d["mains"]) == 0:
        return None

    for side in menu_today.xpath("div[contains(@class, 'menuItem--sidedish')]"):
        side_type = side.find(".//h3").text.strip()
        side_type = side_type.replace("Mensa ","").title()
        side_list = [s.text.strip().replace('\r\n', ' ') for s in side.findall(".//li/strong")]
        menu_d["sides"][side_type] = side_list

    return menu_d


def get_menu_html(menu_d : dict) -> str:
    if (not isinstance(menu_d, dict) or len(menu_d) == 0):
        return None
    menu_s = []

    for t,m in menu_d["mains"].items():
        for name in m["name"]:
            name += f" ({', '.join(m['side'])})" if m["side"] else ""
            menu_s.append('<b>{:s}:</b> <i>{:s}</i>'.format(t, name))

    for t,s in menu_d["sides"].items():
        name = ", ".join(s)
        menu_s.append('<b>{:s}:</b> <i>{:s}</i>'.format(t, name))

    return "\n".join(menu_s)


def get_menu_str(menu_d : dict, msg_id=0) -> str:
    menu_l = []
    menu_l.append(str(int(datetime.utcnow().timestamp()))) # req_ts
    menu_l.append(str(msg_id))
    menu_l.append(menu_d["date"])

    mains_s = []
    for t,m in menu_d["mains"].items():
        for name in m["name"]:
            name += f" ({', '.join(m['side'])})" if m["side"] else ""
            mains_s.append(f"{t}:{name}")
    menu_l.append("+".join(mains_s))

    sides_s = []
    for t,s in menu_d["sides"].items():
        name = ",".join(s)
        sides_s.append(f"{t}:{name}")
    menu_l.append("+".join(sides_s))
    return menu_l


def write_menu_csv(menu_d : dict, msg_id=0, fname='menu.csv'):
    if not menu_d:
        return
    with open(fname, 'a', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile, delimiter=';', quoting=csv.QUOTE_NONE, escapechar="\\")
        row = get_menu_str(menu_d, msg_id=msg_id)
        writer.writerow(row)
    return


## debug
def main():
    menu_d = fetch_menu_dict()
    menu_s = write_menu_csv(menu_d)
    
    menu_s = get_menu_html(menu_d)
    print(menu_s)


if __name__ == "__main__":
    main()
