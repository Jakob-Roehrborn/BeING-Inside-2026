import pandas as pd
import os

from solar_calculation import main_kwp_performance, main_kwp_performance_2025
from heat_pump import heat_pump
from haushalt_csv import household
from Speicher import speicher
import user_json_new as js
from eauto2 import simuliere_e_auto_mit_soc
from kosten_calc2 import berechne_stromkosten_nach_14a_dynamisch
from data_class import output_data
import plotly_diagramme2 as pt

from data_class import input_data


def main_backend(input_user: input_data):
    input_user.general_info.eprice = input_user.general_info.eprice/100
    def timestamp():
        start_date = "2025-01-01 00:00:00"
        end_date = "2025-12-31 23:00:00"
        full_year = pd.date_range(start=start_date, end=end_date, freq='h')
        formatted_timestamps = full_year.strftime('%m-%d %H:00')
        
        return formatted_timestamps

    df = pd.DataFrame()
    df['timestamp'] = timestamp()

    if input_user.solar_system.exist:
        location_user = (input_user.general_info.coordinates.latitude, 
                        input_user.general_info.coordinates.longitude, 
                        input_user.general_info.postal_code)
        
        df['solar'] = main_kwp_performance_2025(input_user)
    else:
        df['solar'] = 0
        
    if input_user.heat_pump.exist:
        df['heat_pump'] = heat_pump(input_user.heat_pump.performance_kWh_year)
    else:
        df['heat_pump'] = 0

    if input_user.ecar.exist:
        ladeleistung = 11 if input_user.ecar.wallbox else 2.7
        df['ecar'] = simuliere_e_auto_mit_soc(input_user.ecar.akku_grosse, input_user.ecar.ziel_jahreskilometer, input_user.ecar.verbrauch_kwh_pro_100km, ladeleistung, input_user.ecar.start_ladezeit, input_user.ecar.anteil_zu_Hause)
    else:
        df['ecar'] = 0

    df['household'] = household()*input_user.general_info.total_consumption      
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

    # KWhJahr * Hausverbrauch + ele_car 
    csv_path = r"material/strompreise_2026_sachsenenergie.csv"
    cols = ["customer_price_gross_ct_per_kwh_konzession_1_32"]
    #df_prices =pd.read_csv(csv_path, usecols=cols, sep=",")
    df_prices =pd.read_csv(csv_path)
    #df["ges_price"] =- df_prices[cols[0]]*df["netz_bezug"]/100 + 0.0778*df['netz_einspeisung']

    df["ges_price"] =- df_prices["customer_price_gross_ct_per_kwh_konzession_1_32"]*df["netz_bezug"]/100+0.0778*df['netz_einspeisung']
    

    df_module = pd.DataFrame()
    df_module, controllable_load, guenstig_m, ersparnis = berechne_stromkosten_nach_14a_dynamisch(df, df_prices)
    df['kosten_konstant'] = (-(-input_user.general_info.eprice * df['netz_bezug'] + 0.0778 * df['netz_einspeisung'])).cumsum()
    df['kosten_dynamisch'] = -df['ges_price'].cumsum()

    df['cumsum_netz_bezug'] = df["netz_bezug"].cumsum()
    df['cumsum_netz_einspeisung'] = df["netz_einspeisung"].cumsum()

    png = False
    pt.plot_grid_exchange_cumsum(df,['cumsum_netz_bezug','cumsum_netz_einspeisung'], rolling_hours = 24*7, title = 'Einspeisung vs Netzbezug', png = png)
    pt.plot_cost(df,['kosten_konstant','kosten_dynamisch'], rolling_hours = 24*7, title = f'Fixer Stromtarife ({input_user.general_info.eprice*100} ct/kWh) vs. Dynamischer Stromtarife', png = png)
    pt.plot_grid_exchange(df,['netz_bezug','netz_einspeisung'], rolling_hours = 24*7, title = 'Einspeisung vs Netzbezug', png = png)

    print('Solar:', df['solar'].sum())


    basisgrundpreis = 70.44  
    grundpreis_netz = 30.00  
    messstelle_imsys = 33.61
    messstelle_mMe = 21.01
    print(df['kosten_dynamisch'].iat[-1]+basisgrundpreis+grundpreis_netz+messstelle_imsys)
    print(df['kosten_konstant'].iat[-1]+basisgrundpreis+grundpreis_netz+messstelle_mMe)
    if input_user.solar_system.exist :
        eigenverbrauch_p = 1-(df["netz_einspeisung"].sum()/(df["solar"]).sum())
    else :
        eigenverbrauch_p = 0
    return output_data( # muss noch angepasst werden 
        netz_einspeisung_kwh = (df["netz_einspeisung"]).sum(),
        netz_bezug_kwh = (df["netz_bezug"]).sum(),
        
        ecar = df['ecar'].sum(),
        solar = df["solar"].sum(),
        household = df["household"].sum(),
        heat_pump = df['heat_pump'].sum(),
        controllable_load = controllable_load, 
        eigenverbrauch_p = eigenverbrauch_p,
        
        cost_dynamic = df['kosten_dynamisch'].iat[-1]+basisgrundpreis+grundpreis_netz+messstelle_imsys, # zu bezahlen für den Kunden = positiv
        cost_const = df['kosten_konstant'].iat[-1]+basisgrundpreis+grundpreis_netz+messstelle_mMe,
        savings_dynamic = df['kosten_konstant'].iat[-1] + messstelle_mMe - df['kosten_dynamisch'].iat[-1] - messstelle_imsys, # Ersparnis mit flexiblem Strompreis
        
        cost_modul_1 = df_module['Modul1'].sum(),
        cost_modul_2 = df_module['Modul2'].sum(),
        cost_modul_3 = df_module['Modul3'].sum(),
        
        guenstig_m =  guenstig_m,
        ersparnis =   ersparnis)


        #eigenverbrauch_p = 1-(df["netz_einspeisung"].sum()/(df["solar"]).sum())

# prüft ob Wetterdaten für eine plz bereits vorhanden ist
def weather_cvs_exists(plz):
    filename = f"solar_base_{plz}_2025.csv"
    file_path = os.path.join('solar_base', filename)
    if os.path.exists(file_path):
        return True
    return False

if __name__ == "__main__":
    input_user = js.load_user_data()
    js.update_config_from_api(input_user)
    main_backend(input_user)
    # df = pd.DataFrame()
    # x, df['smart'] = main_backend(smart=True, ladezeit=13)
    # x, df['nicht'] = main_backend(smart=False, ladezeit=18)
    # print('Smart', df['smart'].iat[-1], 'normal', df['nicht'].iat[-1], 'Ersparnis', df['nicht'].iat[-1]-df['smart'].iat[-1])
    # plot_household_year(df)

