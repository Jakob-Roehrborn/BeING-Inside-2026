# Erstellt csv-Datein mit Wetterdaten für die Berechnung der Solarzelle basierend auf den Koordinaten (Plz)
# Form: mm_dd_hh,ghi_mean,ghi_min,ghi_max,dhi_mean,dhi_min,dhi_max,dni_mean,dni_min,dni_max, tem_mean
# mean: Durchschnitt, min: worst-case, max: best-case
# existiert bereits eine dementsprechende csv-Datei -> keine Neuberechnung
# Quelle der Daten: https://open-meteo.com/
# auf Rat der Experten wird nur noch ein Jahr beachtet (2025)

import requests
import pandas as pd
import time
import os

# ---- Berechnung Durchschnittswerte basierend auf mehreren Jahren ----

def generate_weather_master(lat, lon, plz, start_year=2020, end_year=2025):

    output_dir = r"solar_base"
    if not os.path.exists(output_dir): # erstellt Ordner wenn nicht vorhanden
        os.makedirs(output_dir)
        print(f"Ordner '{output_dir}' erstellt.")

    filename = f"solar_base_{plz}_{start_year}_{end_year}.csv"
    file_path = os.path.join(output_dir, filename)
    if os.path.exists(file_path):
        print(f"--- INFO: Datei {filename} existiert bereits. Daten werden nicht neu berechnet. ---")
        return pd.read_csv(file_path)

    all_data_frames = []

    for year in range(start_year, end_year + 1):
        print(f"Lade Wetterdaten für {year}...")
        url = "https://archive-api.open-meteo.com/v1/archive"
        params = {
            "latitude": lat,
            "longitude": lon,
            "start_date": f"{year}-01-01",
            "end_date": f"{year}-12-31",
            "hourly": "shortwave_radiation,diffuse_radiation,direct_normal_irradiance,temperature_2m",
            "timezone": "UTC" # UTC verhindert DST-Probleme
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
                    'dni': h.get('direct_normal_irradiance'),
                    'temp': h.get('temperature_2m')
                })
        
                df = df[~((df['time'].dt.month == 2) & (df['time'].dt.day == 29))] # ohne Schaltjahre
                all_data_frames.append(df)
            else:
                print(f" Keine Daten für {year}")
        except Exception as e:
            print(f" Fehler im Jahr {year}: {e}")
        
        time.sleep(1.0) 

    if not all_data_frames:
        print("Keine Daten gefunden!")
        return

    full_df = pd.concat(all_data_frames)
    full_df['mm_dd_hh'] = full_df['time'].dt.strftime('%m-%d %H:00')

    master_df = full_df.groupby('mm_dd_hh').agg({ # Gruppierung
        'ghi': ['mean', 'min', 'max'],
        'dhi': ['mean', 'min', 'max'],
        'dni': ['mean', 'min', 'max'],
        'temp': ['mean']
    })

    master_df.columns = [f"{col[0]}_{col[1]}" for col in master_df.columns.values]
    master_df = master_df.reset_index().sort_values('mm_dd_hh')

    master_df.to_csv(file_path, index=False)
    
    print("-" * 30)
    print(f"FERTIG! Datei gespeichert: {file_path}")
    return master_df

# ---- Wetterdaten für ein Jahr laden ----

def generate_weather_2025(lat, lon, plz):
    output_dir = r"solar_base"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Ordner '{output_dir}' erstellt.")

    filename = f"solar_base_{plz}_2025.csv"
    file_path = os.path.join(output_dir, filename)
    
    if os.path.exists(file_path):
        print(f"--- INFO: Datei {filename} existiert bereits. ---")
        return pd.read_csv(file_path)

    url = "https://archive-api.open-meteo.com/v1/archive"
    params = {
        "latitude": lat,
        "longitude": lon,
        "start_date": "2025-01-01",
        "end_date": "2025-12-31",
        "hourly": "shortwave_radiation,diffuse_radiation,direct_normal_irradiance,temperature_2m",
        "timezone": "UTC"
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
                'dni': h.get('direct_normal_irradiance'),
                'temp': h.get('temperature_2m')
            })
            
            df['mm_dd_hh'] = df['time'].dt.strftime('%m-%d %H:00')
            
            final_df = df[['mm_dd_hh', 'ghi', 'dhi', 'dni', 'temp']].copy()
            
            final_df.to_csv(file_path, index=False)
            print("-" * 30)
            print(f"FERTIG! Daten für 2025 gespeichert: {file_path}")
            return final_df
        else:
            print("Keine stündlichen Daten in der API-Antwort gefunden.")
            
    except Exception as e:
        print(f"Fehler beim Abrufen der Daten: {e}")

    return None

