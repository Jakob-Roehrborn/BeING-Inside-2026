# Einträge in user.json ergänzen/ verändern 

import json
import requests
from datetime import datetime

from geopy.geocoders import Nominatim

def get_json_value(keys, json_file='user.json'):
    """
    Navigiert durch ein Dictionary basierend auf einer Liste von Schlüsseln.
    """
    try:
        with open(json_file, 'r') as f:
            current = json.load(f)

        for key in keys:
            current = current[key]
        return current
    except (KeyError, TypeError):
        print(f"Fehler: Der Pfad {keys} wurde nicht gefunden.")
        return None

def geolocate(plz):
    geolocator = Nominatim(user_agent="plz_koordinaten")

    location = geolocator.geocode(plz) # als String!!!

    return location.latitude, location.longitude

def update_config_from_api(json_file):

    with open(json_file, 'r') as f:
        data = json.load(f)
    
    if (plz := data['general_info']['postal_code']):
    
        geolocator = Nominatim(user_agent="plz_koordinaten")

        location = geolocator.geocode(plz) # als String!!!
                    
        # Daten in der JSON aktualisieren
        data['general_info']['coordinates']['latitude'] = location.latitude
        data['general_info']['coordinates']['longitude'] = location.longitude
        data['metadata']['last_updated'] = datetime.now().strftime('%Y-%m-%d')

        print(f'Koordinaten für {plz}: Latitude {location.latitude}, Longitude {location.longitude} ')
                    
        with open(json_file, 'w') as f:
            json.dump(data, f, indent=4)
    else:
        print('update_config_from_api: plz fehlt!')


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

def get_solar_from_user(json_file='user.json'):
    try:
        with open(json_file, 'r') as f:
            data = json.load(f)
        
        # Zugriff über die verschachtelten Schlüssel
        azimuth = data['solar_system']['azimuth']
        tilt = data['solar_system']['tilt']
        capacity_kwp = data['solar_system']['capacity_kwp']
            
        return azimuth, tilt, capacity_kwp

    except FileNotFoundError:
        print(f"Fehler: Die Datei {json_file} wurde nicht gefunden.")
    except KeyError as e:
        print(f"Fehler: Der Schlüssel {e} fehlt in der JSON-Struktur.")
    
    return None, None, None

def get_car_from_user(json_file='user.json'):
    try:
        with open(json_file, 'r') as f:
            data = json.load(f)
        
        # Zugriff über die verschachtelten Schlüssel
        ziel_jahreskilometer = data['electrical_car']['ziel_jahreskilometer']
        verbrauch_kwh_pro_100km = data['electrical_car']['verbrauch_kwh_pro_100km']
        max_leistung_kw = data['electrical_car']['max_leistung_kw']
            
        return ziel_jahreskilometer, verbrauch_kwh_pro_100km, max_leistung_kw

    except FileNotFoundError:
        print(f"Fehler: Die Datei {json_file} wurde nicht gefunden.")
    except KeyError as e:
        print(f"Fehler: Der Schlüssel {e} fehlt in der JSON-Struktur.")
    
    return None, None, None

# Anwendung
#update_config_from_api('user.json')