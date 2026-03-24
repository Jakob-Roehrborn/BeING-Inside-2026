# Erstellt csv-Datein mit Wetterdaten für die Berechnung der Solarzelle
# Form: mm_dd_hh,ghi_mean,ghi_min,ghi_max,dhi_mean,dhi_min,dhi_max,dni_mean,dni_min,dni_max
# mean: Durchschnitt, min: worst-case, max: best-case
# existiert bereits eine dementsprechende csv-Datei -> keine Neuberechnung

import requests
import pandas as pd
import time
import os

from user_json import get_coordinates_from_user, update_config_from_api

# --- TEIL 1: WETTERDATEN HOLEN & STATISTIK ERSTELLEN ---
def generate_weather_master(lat, lon, plz, start_year=2019, end_year=2024):
    
    # erstellt, wenn nicht vorhanden Ordner solar_base
    output_dir = "solar_base"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Ordner '{output_dir}' erstellt.")

    filename = f"solar_base_{plz}_{start_year}_{end_year}.csv"
    file_path = os.path.join(output_dir, filename)
    if os.path.exists(file_path):
        print(f"--- INFO: Datei {filename} existiert bereits. Daten werden nicht neu berechnet. ---")
        return pd.read_csv(file_path)

    all_data_frames = []

    # 3. Historische Daten laden
    for year in range(start_year, end_year + 1):
        print(f"Lade Wetterdaten für {year}...")
        url = "https://archive-api.open-meteo.com/v1/archive"
        params = {
            "latitude": lat,
            "longitude": lon,
            "start_date": f"{year}-01-01",
            "end_date": f"{year}-12-31",
            "hourly": "shortwave_radiation,diffuse_radiation,direct_normal_irradiance",
            "timezone": "UTC" # UTC verhindert DST-Probleme (Sommerzeit)
        }
        
        try:
            res = requests.get(url, params=params)
            data = res.json()
            if 'hourly' in data:
                h = data['hourly']
                df = pd.DataFrame({
                    'time': pd.to_datetime(h.get('time')),
                    'ghi': h.get('shortwave_radiation'),
                    'dhi': h.get('diffuse_radiation'),
                    'dni': h.get('direct_normal_irradiance')
                })
                # Schalttage entfernen für einheitliche 8760 Stunden
                df = df[~((df['time'].dt.month == 2) & (df['time'].dt.day == 29))]
                all_data_frames.append(df)
            else:
                print(f" Keine Daten für {year}")
        except Exception as e:
            print(f" Fehler im Jahr {year}: {e}")
        
        time.sleep(1.0) # API-Schonung

    if not all_data_frames:
        print("Keine Daten gefunden!")
        return

    # 4. Statistiken berechnen (Flattening)
    full_df = pd.concat(all_data_frames)
    full_df['mm_dd_hh'] = full_df['time'].dt.strftime('%m-%d %H:00')

    # Gruppierung: Wir holen Mean, Min und Max für alle drei Strahlungsarten
    master_df = full_df.groupby('mm_dd_hh').agg({
        'ghi': ['mean', 'min', 'max'],
        'dhi': ['mean', 'min', 'max'],
        'dni': ['mean', 'min', 'max']
    })

    # Header flach machen: mm_dd_hh, ghi_mean, ghi_min, ghi_max, ...
    master_df.columns = [f"{col[0]}_{col[1]}" for col in master_df.columns.values]
    master_df = master_df.reset_index().sort_values('mm_dd_hh')

    # 5. Speichern
    #filename = os.path.join(output_dir, f"solar_base_{plz}_{start_year}_{end_year}.csv")
    master_df.to_csv(file_path, index=False)
    
    print("-" * 30)
    print(f"FERTIG! Datei gespeichert: {file_path}")
    print(f"Spalten: {', '.join(master_df.columns.tolist())}")
    return master_df

# --- START ---
#update_config_from_api('user.json')
lat, lon, plz = get_coordinates_from_user('user.json')
weather_data = generate_weather_master(lat, lon, plz, start_year=2020, end_year=2025)