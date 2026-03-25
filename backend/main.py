import pandas as pd
import os

from solar_base import generate_weather_master
from solar_calculation import main_kwp_performance
from heat_pump import heat_pump
from haushalt_csv import household
from Speicher_1 import speicher
#from ploten import plot_auswertung
#from debugprint import debugprints
import user_json_new as js
from eauto2 import simuliere_e_auto_mit_soc
from kosten_calc import berechne_stromkosten_nach_14a
from data_class import output_data

def main_backend():

    def timestamp():
        start_date = "2025-01-01 00:00:00"
        end_date = "2025-12-31 23:00:00"
        full_year = pd.date_range(start=start_date, end=end_date, freq='h')
        formatted_timestamps = full_year.strftime('%m-%d %H:00')
        
        return formatted_timestamps


    input_user = js.load_user_data('user.json')
    js.update_config_from_api(input_user) # setzt die Koordinaten basierend auf der plz
    js.save_user_data(input_user, 'user.json') # speichert die Änderung

    ecar_con = input_user.ecar.ziel_jahreskilometer * input_user.ecar.verbrauch_kwh_pro_100km /100
    heat_pump_con = input_user.heat_pump.performance_kWh_year
    df = pd.DataFrame()
    df['timestamp'] = timestamp()

    if input_user.solar_system.exist:
        location_user = (input_user.general_info.coordinates.latitude, 
                        input_user.general_info.coordinates.longitude, 
                        input_user.general_info.postal_code)
        
        generate_weather_master(*location_user)
        df['solar'] = main_kwp_performance(input_user)
        
    household_con_tot =  input_user.general_info.total_consumption
    if input_user.heat_pump.exist:
        df['heat_pump'] = heat_pump(input_user.heat_pump.performance_kWh_year)
        household_con_tot =  input_user.general_info.total_consumption - heat_pump_con

    if input_user.ecar.exist:
        household_con_tot =  household_con_tot - ecar_con
        ladeleistung = 11 if input_user.ecar.wallbox else 2.7
        df['ecar'] = simuliere_e_auto_mit_soc(input_user.ecar.akku_grosse, input_user.ecar.ziel_jahreskilometer, input_user.ecar.verbrauch_kwh_pro_100km, ladeleistung, input_user.ecar.start_ladezeit)
        
    df['household'] = household(smart = False)*household_con_tot
    df['total_consumption'] = (
        df['household'] + 
        df.get('heat_pump', 0) + 
        df.get('ecar', 0)
    )

    # Berechnung Saldo -> Verbrauch minus Erzeugung
    # Positiv -> Strom aus Netz/Speicher
    # Negativ ->  Überschuss für Speicher/Netzeinspeisung
    df['saldo'] = df['total_consumption'] - df.get('solar', 0)

    if input_user.memory.exist:
        speicher_letzt = 0
        speicher_kap = input_user.memory.capacity_kWh
    
        speicher_stand_liste = []
        netz_bezug_liste = []
        netz_einspeisung_liste = []
        
        for saldo in df['saldo']:
            speicher_letzt, uebrig_laden, uebrig_entladen = speicher(saldo, speicher_kap, speicher_letzt)
            
            speicher_stand_liste.append(speicher_letzt)
            netz_bezug_liste.append(uebrig_entladen)
            netz_einspeisung_liste.append(uebrig_laden)
            
        df['speicher_stand'] = speicher_stand_liste
        df['netz_bezug'] = netz_bezug_liste
        df['netz_einspeisung'] = netz_einspeisung_liste

    else:
        # Wenn kein Speicher existiert, ist das Saldo direkt unser Netzbezug/Einspeisung
        # df.clip(lower=0) -> alle negativen Zahlen zu 0
        df['netz_bezug'] = df['saldo'].clip(lower=0) 
        df['netz_einspeisung'] = df['saldo'].clip(upper=0).abs()

    print('Haushalt:', (df["household"]).sum())
    print('Solar:', (df["solar"]).sum())
    print('Netzeinspeisung:', (df["netz_einspeisung"]).sum())
    print('Netzbezug:', (df["netz_bezug"]).sum())
    print('Gesamtpreis:', (df['ges_price']).sum())
    print('Gesamtverbrauch:', df['total_consumption'].min())
    

    # KWhJahr * Hausverbrauch + ele_car 
    csv_path = "material\strompreise_2026_sachsenenergie.csv"
    cols = ["customer_price_gross_ct_per_kwh_konzession_1_32"]
    df_prices =pd.read_csv(csv_path, usecols=cols, sep=",")
    df["ges_price"] =- df_prices[cols[0]]*df["netz_bezug"]/100+0.0778*df['netz_einspeisung']

    berechne_stromkosten_nach_14a(df)
    df.to_csv("test_df.csv", index=False)
   
    return output_data( # muss noch angepasst werden 
        netz_einspeisung_kwh = (df["netz_einspeisung"]).sum(),
        netz_bezug_kwh = (df["netz_bezug"]).sum(),
        gesamtkosten_euro = (df['ges_price']).sum()
    ) 

# prüft ob Wetterdaten für eine plz bereits vorhanden ist
def weather_cvs_exists(plz):
    filename = f"solar_base_{plz}_2020_2025.csv"
    file_path = os.path.join('solar_base', filename)
    if os.path.exists(file_path):
        return True
    return False

if __name__ == "__main__":
    main_backend()

