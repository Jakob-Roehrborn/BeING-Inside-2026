from solar_base import generate_weather_master
from solar_calculation import main_kwp_performance
from heat_pump import heat_pump
from eauto import optimierte_ladesimulation
from haushalt_csv import household
from Speicher_1 import speicher 

import pandas as pd
import user_json_new as js

from data_class import input_data

import matplotlib.pyplot as plt


def main_backend(input_user: input_data):

    def timestamp():
        start_date = "2025-01-01 00:00:00"
        end_date = "2025-12-31 23:00:00"
        full_year = pd.date_range(start=start_date, end=end_date, freq='h')
        formatted_timestamps = full_year.strftime('%m-%d %H:00')
        
        return formatted_timestamps


    js.update_config_from_api(input_user) # setzt die Koordinaten basierend auf der plz
    js.save_user_data(input_user, 'user.json') # speichert die Änderung

    ecar_con = input_user.ecar.ziel_jahreskilometer * input_user.ecar.verbrauch_kwh_pro_100km /100
    heatpump_con = input_user.heat_pump.performance_kWh_year
    household_con_tot =  input_user.general_info.total_consumption - ecar_con - heatpump_con
    df = pd.DataFrame()
    df['timestamp'] = timestamp()

    df['household'] = household()*household_con_tot

    if input_user.solar_system.exist:
        location_user = (input_user.general_info.coordinates.latitude, 
                        input_user.general_info.coordinates.longitude, 
                        input_user.general_info.postal_code)
        
        generate_weather_master(*location_user)
        df['solar'] = main_kwp_performance(input_user) 

    if input_user.heat_pump.exist:
        df['heat_pump'] = heat_pump(input_user.heat_pump.performance_kWh_year)

    if input_user.ecar.exist:
    
        ladeleistung = 11 if input_user.ecar.wallbox else 2.7
        df['ecar'] = optimierte_ladesimulation(
            input_user.ecar.ziel_jahreskilometer,
            input_user.ecar.verbrauch_kwh_pro_100km, 
            ladeleistung).values # .values -> ignoriert Index
        
    # 1. Gesamten Verbrauch berechnen (wir nutzen .get(), falls eine Spalte nicht existiert, wird 0 genommen)
    df['total_consumption'] = (
        df['household'] + 
        df.get('heat_pump', 0) + 
        df.get('ecar', 0)
    )

    # 2. Saldo berechnen: Verbrauch minus Erzeugung
    # Positiv = Wir brauchen Strom aus dem Netz/Speicher
    # Negativ = Wir haben Überschuss für den Speicher/Netzeinspeisung
    df['saldo'] = df['total_consumption'] - df.get('solar', 0)
    # 3. Speicher-Simulation durchführen
    if input_user.memory.exist:
        speicher_letzt = 0
        speicher_kap = input_user.memory.capacity_kWh
        
        # Listen vorab erstellen (viel schneller als das DataFrame in der Schleife zu verändern)
        speicher_stand_liste = []
        netz_bezug_liste = []
        netz_einspeisung_liste = []
        
        # Wir iterieren nur über die Saldo-Werte
        for saldo in df['saldo']:
            # Funktion aus Speicher.py aufrufen
            speicher_letzt, uebrig_laden, uebrig_entladen = speicher(saldo, speicher_kap, speicher_letzt)
            
            # Ergebnisse für diese Stunde speichern
            speicher_stand_liste.append(speicher_letzt)
            netz_bezug_liste.append(uebrig_entladen)
            netz_einspeisung_liste.append(uebrig_laden)
            
        # Die fertigen Listen als neue Spalten ans DataFrame anhängen
        df['speicher_stand'] = speicher_stand_liste
        df['netz_bezug'] = netz_bezug_liste
        df['netz_einspeisung'] = netz_einspeisung_liste

    else:
        # Wenn kein Speicher existiert, ist das Saldo direkt unser Netzbezug/Einspeisung
        # df.clip(lower=0) macht alle negativen Zahlen zu 0
        df['netz_bezug'] = df['saldo'].clip(lower=0) 
        df['netz_einspeisung'] = df['saldo'].clip(upper=0).abs()

    # Ganz am Ende speichern
    df.to_csv("test_df.csv", index=False)
    # KWhJahr * Hausverbrauch + ele_car 
    csv_path = "material\strompreise_2026_sachsenenergie.csv"
    cols = ["customer_price_gross_ct_per_kwh_konzession_1_32"]
    df_prices =pd.read_csv(csv_path, usecols=cols, sep=",")
    df["ges_price"] =- df_prices[cols[0]]*df["netz_bezug"]/100+0.0778*df['netz_einspeisung']

    print('Haushalt:', (df["household"]).sum())
    print('Solar:', (df["solar"]).sum())
    print('Netzeinspeisung:', (df["netz_einspeisung"]).sum())
    print('Netzbezug:', (df["netz_bezug"]).sum())
    print('Gesamtpreis:', (df['ges_price']).sum())
    print('Gesamtverbrauch:', df['total_consumption'].min())
    
    df.to_csv("test_df.csv", index=False)
   
    return (df["netz_einspeisung"]).sum(), (df["netz_bezug"]).sum(), (df['ges_price']).sum()

if __name__ == "__main__":
    main_backend(js.load_user_data('user.json'))
    