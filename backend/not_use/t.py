def calculate_tilted_irradiance(csv_path, tilt, azimuth, lat, lon, scenario='mean'):
    """
    Berechnet die Einstrahlung auf einer geneigten Fläche.
    scenario: 'mean', 'min' oder 'max' (entspricht den Suffixen in der Master-CSV)
    """

    df = pd.read_csv(csv_path)
    df = df.sort_values('mm_dd_hh')
    
    # Zeitstempel für die Geometrie (UTC)
    # fiktives Jahr 2023 für die Sonnenstandsberechnung
    times = pd.to_datetime("2023-" + df['mm_dd_hh'], format="%Y-%m-%d %H:%M")
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

def add_performance_column(df, kwp_anlage, efficiency = 0.85):
    """
    Berechnet die Leistung und gibt nur Zeitstempel und Performance zurück.
    """

    df_result = df.copy()
    df_result['solar'] = (df_result['leistung_geneigt'] / 1000) * kwp_anlage * efficiency

    # Nur die gewünschten Spalten - doppelte Klammer [[...]] gibt ein DataFrame zurück
    df_reduced = df_result[['solar']] #'mm_dd_hh',
    
    return df_reduced

def main_kwp_performance(user):
    csv_path = os.path.join("solar_base", f"solar_base_{user.general_info.postal_code}_2020_2025.csv")
  
    ergebnis_df = calculate_tilted_irradiance(csv_path, 
                                            user.solar_system.tilt,
                                            user.solar_system.azimuth, 
                                            user.general_info.coordinates.latitude, 
                                            user.general_info.coordinates.longitude,
                                            scenario='mean')
    
    return add_performance_column(ergebnis_df, user.solar_system.capacity_kwp)