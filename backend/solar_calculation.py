# Quelle: https://www.photovoltaikforum.com/core/article/126-das-temperaturverhalten-von-pv-modulen/
# pvlib: https://github.com/pvlib/pvlib-python

import solar_base as solar_csv

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

def calculate_tilted_irradiance_2025(df, tilt, azimuth, lat, lon, year = 2025):

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

# ---- NOCT-Modell ----
def performance_NOCT(df, kwp_anlage, efficiency = 0.85): # efficiency des Wechselrichter & Kabel

    df_result = df.copy()
    gamma = -0.004  # Temperaturkoeffizient pro K
    t_ref = 25      # Referenztemperatur STC
    temp_air = df_result['temp'] if 'temp' in df_result.columns else 15
    t_cell = temp_air + (df_result['leistung_geneigt'] / 800) * 25 # Zelltemperatur Annahme NOCT = 45 °C.
    temp_factor = 1 + gamma * (t_cell - t_ref)

    df_result['solar'] = (df_result['leistung_geneigt'] / 1000) * kwp_anlage * efficiency * temp_factor    
    df_result['solar'] = df_result['solar'].clip(lower=0) # keine negativen Werte
    df_reduced = df_result[['solar']]
    
    return df_reduced

# ---- Zelltemperatur mit pvlib ----
# Beachtet den Wind bei der Zelltemperaturberechnung

def performance_pvlib(df, kwp_anlage, efficiency=0.85):

    # pvlib zur Zelltemperatur mit SAPM Modell
    # freistehend -> open_rack_glass_polymer 
    # dachintegriert -> insulated_back_glass_polymer
    # Glas-Gals freistehend -> glass_glass_open_rack
    # industrielle Montagesysteme -> open_rack_glass_steel

    temp_params = pvlib.temperature.TEMPERATURE_MODEL_PARAMETERS['sapm']['insulated_back_glass_polymer']
    wind_speed = df['wind_speed'] if 'wind_speed' in df.columns else 2 # ergänzt die Spalte wind_speed wenn wind_speed nicht definiert
    
    t_cell = pvlib.temperature.sapm_cell(
        poa_global=df['leistung_geneigt'],
        temp_air=df['temp'],
        wind_speed=wind_speed,
        **temp_params
    )
    gamma = -0.004 # Temperaturkoeffizient
    t_ref = 25
    
    temp_factor = 1 + gamma * (t_cell - t_ref)
    p_dc = (df['leistung_geneigt'] / 1000) * kwp_anlage * temp_factor
    df['solar'] = p_dc * efficiency # Wechselrichter-Verluste = efficiency
    
    return df[['solar']].clip(lower=0)

def main_kwp_performance_2025(user, year = 2025, wind = True):

    df = solar_csv.generate_weather_2025_windspeed(user.general_info.coordinates.latitude, 
                    user.general_info.coordinates.longitude, 
                    user.general_info.postal_code)
      
    ergebnis_df = calculate_tilted_irradiance_2025(df, 
                                            user.solar_system.tilt,
                                            user.solar_system.azimuth, 
                                            user.general_info.coordinates.latitude, 
                                            user.general_info.coordinates.longitude,
                                            year= year)
    
    return performance_pvlib(ergebnis_df, user.solar_system.capacity_kwp) if wind else performance_NOCT(ergebnis_df, user.solar_system.capacity_kwp)
    #return performance_NOCT(ergebnis_df, user.solar_system.capacity_kwp) # ohne Beachtung des Windes