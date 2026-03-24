import pandas as pd
import pvlib
import numpy as np
import os

from user_json import get_coordinates_from_user, get_solar_from_user

def calculate_tilted_irradiance(csv_path, tilt, azimuth, lat, lon, scenario='mean'):
    """
    Berechnet die Einstrahlung auf einer geneigten Fläche.
    scenario: 'mean', 'min' oder 'max' (entspricht den Suffixen in der Master-CSV)
    """
    # 1. Master-CSV Laden
    df = pd.read_csv(csv_path)
    df = df.sort_values('mm_dd_hh')
    
    # 2. Zeitstempel für die Geometrie (UTC)
    # fiktives Jahr 2023 für die Sonnenstandsberechnung
    times = pd.to_datetime("2023-" + df['mm_dd_hh'], format="%Y-%m-%d %H:%M")
    times_utc = times.dt.tz_localize('UTC')

    # 3. Sonnenstand berechnen
    solpos = pvlib.solarposition.get_solarposition(times_utc, lat, lon)
    
    # Längen-Check (Sicherheitsnetz)
    if len(solpos) != len(df):
        solpos = solpos.iloc[:len(df)]

    # 4. Spalten dynamisch wählen (z.B. ghi_mean, ghi_min, etc.)
    dni_data = df[f'dni_{scenario}'].to_numpy()
    ghi_data = df[f'ghi_{scenario}'].to_numpy()
    dhi_data = df[f'dhi_{scenario}'].to_numpy()

    # 5. Einstrahlung berechnen
    total_irrad = pvlib.irradiance.get_total_irradiance(
        surface_tilt=tilt,
        surface_azimuth=azimuth,
        dni=dni_data,
        ghi=ghi_data,
        dhi=dhi_data,
        solar_zenith=solpos['zenith'].to_numpy(),
        solar_azimuth=solpos['azimuth'].to_numpy()
    )
    
    # Ergebnis in neuen Spalte speichern
    df['leistung_geneigt'] = total_irrad['poa_global']
    
    return df

def performance_per_area(df, monat, tag, stunde):
    such_string = f"{monat:02d}-{tag:02d} {stunde:02d}:00"
    ergebnis = df[df['mm_dd_hh'] == such_string]
    if not ergebnis.empty:
        return ergebnis['leistung_geneigt'].iloc[0]
    return 0.0

def performance_kw(df, monat, tag, stunde, kwp_anlage):
    such_string = f"{monat:02d}-{tag:02d} {stunde:02d}:00"
    ergebnis = df[df['mm_dd_hh'] == such_string]
    if not ergebnis.empty:
        strahlung = ergebnis['leistung_geneigt'].iloc[0]
        return (strahlung / 1000) * kwp_anlage
    return 0.0

def add_performance_column(df, kwp_anlage):
    """
    Berechnet die Leistung und gibt nur Zeitstempel und Performance zurück.
    """

    df_result = df.copy()
    df_result['solar'] = (df_result['leistung_geneigt'] / 1000) * kwp_anlage

    # Nur die gewünschten Spalten - doppelte Klammer [[...]] gibt ein DataFrame zurück
    df_reduced = df_result[['solar']] #'mm_dd_hh',
    
    return df_reduced

def performance_range_sum(df, start_str, end_str, capacity_kwp):
    """
    Summiert die Leistung über eine Zeitspanne, indem sie 
    die bestehende Funktion 'performance_kw' für jede Stunde aufruft.
    """
    # 1. Zeitspanne generieren (fiktives Jahr 2023 für die Logik)
    # Wir erstellen eine Liste aller Stunden zwischen Start und Ende
    start_dt = pd.to_datetime("2023-" + start_str, format="%Y-%m-%d %H:%M")
    end_dt = pd.to_datetime("2023-" + end_str, format="%Y-%m-%d %H:%M")
    
    # Generiere alle Stunden-Zeitstempel in diesem Bereich
    hour_range = pd.date_range(start=start_dt, end=end_dt, freq='h')
    
    total_kwh = 0.0
    
    # 2. Die bestehende Funktion für jede Stunde aufrufen
    for current_dt in hour_range:
        m = current_dt.month
        d = current_dt.day
        h = current_dt.hour
        
        # Aufruf deiner Original-Funktion
        # Da die Funktion kW zurückgibt und wir über 1 Stunde summieren,
        # ist kW * 1h = kWh.
        stunden_ertrag = performance_kw(df, m, d, h, capacity_kwp)
        total_kwh += stunden_ertrag
        
    return total_kwh

def time_range(ergebnis_df, start_str, end_str, capacity_kwp):
        ergebnis = performance_range_sum(ergebnis_df, start_str, end_str, capacity_kwp)
        print(f"Produzierter Strom im Zeitraum {start_str} - {end_str}: {ergebnis:.2f} kWh")


def main_kwp_performance(lat, lon, plz):
    csv_path = os.path.join("solar_base", f"solar_base_{plz}_2020_2025.csv")
    azimuth, tilt, capacity_kwp = get_solar_from_user('user.json')
    ergebnis_df = calculate_tilted_irradiance(csv_path, tilt, azimuth, lat, lon, scenario='mean')
    return add_performance_column(ergebnis_df, capacity_kwp)

# JSON-Daten
# lat, lon, plz = get_coordinates_from_user('user.json')
# azimuth, tilt, capacity_kwp = get_solar_from_user('user.json')

# # Pfad zur Master-Wetterdatei im solar_base Ordner
# data = os.path.join("solar_base", f"solar_base_{plz}_2020_2025.csv")

# WAHL = 'mean' # SZENARIO: 'mean', 'min' oder 'max'

# try:
#     # Berechnung mit dem gewählten Szenario
#     ergebnis_df = calculate_tilted_irradiance(data, azimuth, tilt, lat, lon, scenario=WAHL)

#     if capacity_kwp is not None:
#         print(f"\n--- BERECHNUNG FÜR SZENARIO: {WAHL.upper()} ---")
#         print(f"Jahresertrag ({capacity_kwp} kWp): {(ergebnis_df['leistung_geneigt'].sum() / 1000 * capacity_kwp):,.2f} kWh")

#         # Beispielabfrage 02.03. 12:00
#         p_kw = performance_kw(ergebnis_df, 3, 2, 12, capacity_kwp)
#         print(f"Leistung am 02.03. 12:00: {p_kw:.2f} kW")

#         start_str = "01-01 00:00"
#         end_str = "12-31 23:00" #mm-dd
#         time_range(start_str, end_str)

# except Exception as e:
#     print(f"Fehler: {e}")
#     import traceback
#     traceback.print_exc()