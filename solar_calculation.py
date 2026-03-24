import pandas as pd
import pvlib
import numpy as np
import os

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

# --- ANWENDUNG ---
PLZ = "01067"
# Pfad zur Master-Wetterdatei im solar_base Ordner
DATEI = os.path.join("solar_base", f"weather_master_{PLZ}.csv")

BREITE, LAENGE = 51.05, 13.74
NEIGUNG, AUSRICHTUNG = 35, 180 
USER_KWP = 10.0
WAHL = 'mean' # SZENARIO: 'mean', 'min' oder 'max'

try:
    # Berechnung mit dem gewählten Szenario
    ergebnis_df = calculate_tilted_irradiance(DATEI, NEIGUNG, AUSRICHTUNG, BREITE, LAENGE, scenario=WAHL)

    print(f"\n--- BERECHNUNG FÜR SZENARIO: {WAHL.upper()} ---")
    print(f"Jahresertrag ({USER_KWP} kWp): {(ergebnis_df['leistung_geneigt'].sum() / 1000 * USER_KWP):,.2f} kWh")

    # Beispielabfrage 02.03. 12:00
    p_kw = performance_kw(ergebnis_df, 3, 2, 12, USER_KWP)
    print(f"Leistung am 02.03. 12:00: {p_kw:.2f} kW")

except Exception as e:
    print(f"Fehler: {e}")
    import traceback
    traceback.print_exc()