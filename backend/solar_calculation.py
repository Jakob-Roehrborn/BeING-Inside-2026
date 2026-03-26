# Quelle: https://www.photovoltaikforum.com/core/article/126-das-temperaturverhalten-von-pv-modulen/

import pandas as pd
import pvlib
import numpy as np
import os

def calculate_tilted_irradiance(csv_path, tilt, azimuth, lat, lon, scenario='mean'):

    df = pd.read_csv(csv_path)
    df = df.sort_values('mm_dd_hh')
    
    times = pd.to_datetime("2025-" + df['mm_dd_hh'], format="%Y-%m-%d %H:%M") # fiktives Jahr 2025 für die Sonnenstandsberechnung
    times_utc = times.dt.tz_localize('UTC')

    solpos = pvlib.solarposition.get_solarposition(times_utc, lat, lon) # berechnet Sonnenstand
    
    if len(solpos) != len(df):
        solpos = solpos.iloc[:len(df)]

    dni_data = df[f'dni_{scenario}'].to_numpy()
    ghi_data = df[f'ghi_{scenario}'].to_numpy()
    dhi_data = df[f'dhi_{scenario}'].to_numpy()

    total_irrad = pvlib.irradiance.get_total_irradiance( # Berechnung Einstrahlung
        surface_tilt=tilt,
        surface_azimuth=azimuth,
        dni=dni_data,
        ghi=ghi_data,
        dhi=dhi_data,
        solar_zenith=solpos['zenith'].to_numpy(),
        solar_azimuth=solpos['azimuth'].to_numpy()
    )

    df['leistung_geneigt'] = total_irrad['poa_global']
    
    return df

def performance_column(df, kwp_anlage, efficiency = 0.85): # efficiency des Wechselrichter & Kabel

    df_result = df.copy()
    gamma = -0.004  # Temperaturkoeffizient pro K
    t_ref = 25      # Referenztemperatur STC
    temp_air = df_result['temp_mean'] if 'temp_mean' in df_result.columns else 15
    t_cell = temp_air + (df_result['leistung_geneigt'] / 800) * 25 # Zelltemperatur Annahme NOCT = 45 °C.
    temp_factor = 1 + gamma * (t_cell - t_ref)

    df_result['solar'] = (df_result['leistung_geneigt'] / 1000) * kwp_anlage * efficiency * temp_factor
    # df_result['solar2'] = (df_result['leistung_geneigt'] / 1000) * kwp_anlage * efficiency # ohne Temperatureinfluss
    #plot_data(df_result, ['solar','solar2'], title='Solar Temperatureinfluss')
    
    df_result['solar'] = df_result['solar'].clip(lower=0) # keine negativen Werte
    df_reduced = df_result[['solar']]
    
    return df_reduced

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

def main_kwp_performance(user):
    csv_path = os.path.join(r"solar_base", f"solar_base_{user.general_info.postal_code}_2020_2025.csv")
  
    ergebnis_df = calculate_tilted_irradiance(csv_path, 
                                            user.solar_system.tilt,
                                            user.solar_system.azimuth, 
                                            user.general_info.coordinates.latitude, 
                                            user.general_info.coordinates.longitude,
                                            scenario='mean')
    
    return performance_column(ergebnis_df, user.solar_system.capacity_kwp)


# ---- nur für 2025 -----

def calculate_tilted_irradiance_2025(csv_path, tilt, azimuth, lat, lon, year = 2025):

    df = pd.read_csv(csv_path)
    df = df.sort_values('mm_dd_hh')

    times = pd.to_datetime(f"{year}-" + df['mm_dd_hh'], format="%Y-%m-%d %H:%M")
    times_utc = times.dt.tz_localize('UTC')
    solpos = pvlib.solarposition.get_solarposition(times_utc, lat, lon)

    if len(solpos) != len(df):
        solpos = solpos.iloc[:len(df)]

    dni_data = df['dni'].to_numpy()
    ghi_data = df['ghi'].to_numpy()
    dhi_data = df['dhi'].to_numpy()

    total_irrad = pvlib.irradiance.get_total_irradiance(
        surface_tilt=tilt,
        surface_azimuth=azimuth,
        dni=dni_data,
        ghi=ghi_data,
        dhi=dhi_data,
        solar_zenith=solpos['zenith'].to_numpy(),
        solar_azimuth=solpos['azimuth'].to_numpy()
    )

    df['leistung_geneigt'] = total_irrad['poa_global']
    
    return df

def performance_column_2025(df, kwp_anlage, efficiency = 0.85): # efficiency des Wechselrichter & Kabel

    df_result = df.copy()
    gamma = -0.004  # Temperaturkoeffizient pro K
    t_ref = 25      # Referenztemperatur STC
    temp_air = df_result['temp'] if 'temp' in df_result.columns else 15
    t_cell = temp_air + (df_result['leistung_geneigt'] / 800) * 25 # Zelltemperatur Annahme NOCT = 45 °C.
    temp_factor = 1 + gamma * (t_cell - t_ref)

    df_result['solar'] = (df_result['leistung_geneigt'] / 1000) * kwp_anlage * efficiency * temp_factor
    # df_result['solar2'] = (df_result['leistung_geneigt'] / 1000) * kwp_anlage * efficiency # ohne Temperatureinfluss
    #plot_data(df_result, ['solar','solar2'], title='Solar Temperatureinfluss')
    
    df_result['solar'] = df_result['solar'].clip(lower=0) # keine negativen Werte
    df_reduced = df_result[['solar']]
    
    return df_reduced

def main_kwp_performance_2025(user, year = 2025):
    csv_path = os.path.join(r"solar_base", f"solar_base_{user.general_info.postal_code}_{year}.csv")
  
    ergebnis_df = calculate_tilted_irradiance_2025(csv_path, 
                                            user.solar_system.tilt,
                                            user.solar_system.azimuth, 
                                            user.general_info.coordinates.latitude, 
                                            user.general_info.coordinates.longitude,
                                            year= year)
    
    return performance_column_2025(ergebnis_df, user.solar_system.capacity_kwp)