# Einträge in user.json ergänzen/ verändern 

import json
import requests
from datetime import datetime

def update_config_from_api(json_file):
    # 1. JSON laden
    try:
        with open(json_file, 'r') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"Fehler: {json_file} nicht gefunden.")
        return

    plz = data['general_info']['postal_code']
    
    # 2. Koordinaten abrufen (Zippopotam API)
    print(f"Suche Koordinaten und Stadt für PLZ {plz}...")
    try:
        response = requests.get(f"http://api.zippopotam.us/de/{plz}")
        if response.status_code == 200:
            loc_data = response.json()['places'][0]
            
            # Daten extrahieren
            lat = float(loc_data['latitude'])
            lon = float(loc_data['longitude'])
            city = loc_data['place name']
            
            # 3. Felder in der Dictionary-Struktur aktualisieren
            data['general_info']['coordinates']['latitude'] = lat
            data['general_info']['coordinates']['longitude'] = lon
            data['general_info']['city'] = city
            
            # Datum auf heute setzen (Format: 2024-05-22)
            data['metadata']['last_updated'] = datetime.now().strftime('%Y-%m-%d')
            
            # 4. JSON Datei speichern (mit Einrückung für Lesbarkeit)
            with open(json_file, 'w') as f:
                json.dump(data, f, indent=4)
            
            print(f"Erfolgreich aktualisiert: {city} (Lat: {lat}, Lon: {lon})")
            print(f"Zeitstempel gesetzt auf: {data['metadata']['last_updated']}")
        else:
            print(f"PLZ {plz} wurde von der API nicht gefunden.")
            
    except Exception as e:
        print(f"Ein Fehler ist aufgetreten: {e}")


def get_coordinates_from_user(json_file='user.json'):
    try:
        with open(json_file, 'r') as f:
            data = json.load(f)
        
        # Zugriff über die verschachtelten Schlüssel
        lat = data['general_info']['coordinates']['latitude']
        lon = data['general_info']['coordinates']['longitude']
        plz = data['general_info']['postal_code']
        
        # Prüfung, ob die Werte schon gesetzt wurden (nicht null sind)
        if lat is None or lon is None:
            print("Warnung: Koordinaten sind noch nicht in der JSON gesetzt!")
            return None, None, None
            
        return lat, lon, plz

    except FileNotFoundError:
        print(f"Fehler: Die Datei {json_file} wurde nicht gefunden.")
    except KeyError as e:
        print(f"Fehler: Der Schlüssel {e} fehlt in der JSON-Struktur.")
    
    return None, None, None

# Anwendung
#update_config_from_api('user.json')