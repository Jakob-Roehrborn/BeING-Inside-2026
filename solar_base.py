# Erstellt csv-Datein mit Wetterdaten für die Berechnung der Solarzelle basierend auf der Postleitzahl
# Form: mm_dd_hh,ghi_mean,ghi_min,ghi_max,dhi_mean,dhi_min,dhi_max,dni_mean,dni_min,dni_max
# mean: Durchschnitt, min: worst-case, max: best-case

import requests
import pandas as pd
import time
import os

# --- TEIL 1: WETTERDATEN HOLEN & STATISTIK ERSTELLEN ---
def generate_weather_master(plz, start_year=2019, end_year=2024):
    # 1. Ordner erstellen
    output_dir = "solar_base"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Ordner '{output_dir}' erstellt.")

    # 2. Koordinaten abrufen
    geo_url = f"http://api.zippopotam.us/de/{plz}"
    
    try:
        geo_res = requests.get(geo_url)
        if geo_res.status_code == 200:
            loc = geo_res.json()['places'][0]
            lat, lon = float(loc['latitude']), float(loc['longitude'])
            if not (47 < lat < 55): lat, lon = 51.05, 13.74
        print(f"Koordinaten für {plz}: {lat}, {lon}")
    except:
        print("Nutze Fallback-Koordinaten.")

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
    filename = os.path.join(output_dir, f"solar_base_{plz}.csv")
    master_df.to_csv(filename, index=False)
    
    print("-" * 30)
    print(f"FERTIG! Datei gespeichert: {filename}")
    print(f"Spalten: {', '.join(master_df.columns.tolist())}")
    return master_df

# --- START ---
plz = "01067"
#plz = "01445"
weather_data = generate_weather_master(plz, start_year=2020, end_year=2025)