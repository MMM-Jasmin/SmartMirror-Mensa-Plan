#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from mensa_api import *
import json, os
from datetime import date

def fromDictToJson(menu_d : dict) -> str:

    json_object = json.dumps(menu_d) 
    return json_object


def main():
    response_file_path = os.path.dirname(__file__) + '/mensa_response.json'

    try:
        menu_d = fetch_menu_dict()
    
        today = date.today()
        formatted_date = today.strftime('%d %B %Y')
        menu_d["date"] = formatted_date
    
        menu_j = fromDictToJson(menu_d)
        
        with open(response_file_path, 'w') as f:
            json.dump(menu_j, f)

    except:
        f = open(response_file_path)
        menu_j = json.load(f)

    print(menu_j)

if __name__ == "__main__":
    main()


"""
{"MensaPlan": ["2020-02-04\n", [{"name": "Tagesmen\u00fc", "value": "Schweineschnitzel mit Champignonrahmso\u00dfe"}, 
{"name": "Vegetarisch", "value": "Sp\u00e4tzlepfanne mit Pilzen und Gem\u00fcse, dazu Paprikaso\u00dfe"}, 
{"name": "Eintopf", "value": "Schnittbohneneintopf"}, {"name": "Eintopf / Suppe", "value": "Pekingsuppe"}, 
{"name": "Mensa vital", "value": "Karamellisiertes Putensteak mit Kartoffelp\u00fcree, Bratenjus und Sesam-Blumenkohl, dazu eine Banane"}, 
{"name": "Aktions-Theke", "value": "H\u00e4hnchenbrust in Parmesan-Ei-H\u00fclle, dazu Bandnudeln und mediterranes Gem\u00fcse"}, 
{"name": "Aktions-Theke", "value": "Ofenkartoffel mit Antipasti und Sauerrahm"}, 
{"name": "Aktions-Theke", "value": "Ofenkartoffel mit Sour Cream und R\u00e4ucherlachs"}, 
{"name": "Dessertbuffet", "value": "T\u00e4glich wechselnde Dessertvariationen., Hausgemachte Milchshakes"}, 
{"name": "Sides", "value": "Rosmarinkartoffeln, Gem\u00fcse-Couscous, Erbsen-M\u00f6hrengem\u00fcse, Romanobohnen, Beilagensalate, G\u00f6tterspeise, Brombeer-Kokos-Quark, Karamell-Vanille-Pudding, Eis"}]]}
"""

