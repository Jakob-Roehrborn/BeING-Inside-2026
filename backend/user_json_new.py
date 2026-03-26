import json
from datetime import datetime
from geopy.geocoders import Nominatim
# Importiere deine Klassen und die Umwandlungsfunktion
from data_class import input_to_class, input_data 

def load_user_data(json_file = r"user.json") -> input_data:
    """Lädt die JSON und gibt ein EnergyData Objekt zurück."""
    with open(json_file, 'r', encoding='utf-8') as f:
        raw_data = json.load(f)
    return input_to_class(raw_data)

def save_user_data(obj: input_data, json_file=r'user.json'):
    # Verwandelt das Objekt und alle Unterobjekte zurück in ein Dict
    import dataclasses
    data_as_dict = dataclasses.asdict(obj)
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(data_as_dict, f, indent=4)

def update_config_from_api(user_obj: input_data):
    """Aktualisiert Koordinaten direkt im Objekt."""
    plz = user_obj.general_info.postal_code
    
    if plz:
        geolocator = Nominatim(user_agent="plz_koordinaten")
        location = geolocator.geocode(plz)
        
        if location:
            # Werte direkt im Objekt setzen (Punkt-Notation!)
            user_obj.general_info.coordinates.latitude = location.latitude
            user_obj.general_info.coordinates.longitude = location.longitude
            user_obj.metadata.last_updated = datetime.now().strftime('%Y-%m-%d')
            
            print(f'Koordinaten für {plz} aktualisiert: {location.latitude}, {location.longitude}')
        else:
            print(f"PLZ {plz} konnte nicht gefunden werden.")
    else:
        print('update_config_from_api: PLZ fehlt im Objekt!')
