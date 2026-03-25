#from user_json import update_config_from_api, get_json_value, get_coordinates_from_user, get_ecar_from_user
from solar_base import generate_weather_master
from solar_calculation import main_kwp_performance
from heat_pump import heat_pump
from eauto import optimierte_ladesimulation
from haushalt_csv import household

from data_class import input_to_class

import pandas as pd
import user_json_new as js

def timestamp():
    start_date = "2025-01-01 00:00:00"
    end_date = "2025-12-31 23:00:00"
    full_year = pd.date_range(start=start_date, end=end_date, freq='h')
    formatted_timestamps = full_year.strftime('%m-%d %H:00')
    
    return formatted_timestamps


input_user = js.load_user_data('user.json')

js.update_config_from_api(input_user) # setzt die Koordinaten basierend auf der plz
js.save_user_data(input_user, 'user.json') # speichert die Änderung

df = pd.DataFrame()
df['timestamp'] = timestamp()

df['household'] = household(input_user.general_info.total_consumption)/1000

if input_user.solar_system.exist:
    location_user = (input_user.general_info.coordinates.latitude, 
                     input_user.general_info.coordinates.longitude, 
                     input_user.general_info.postal_code)
    
    generate_weather_master(*location_user)
    df['solar'] = main_kwp_performance(input_user) # df mit Spalten: mm_dd_hh, performance_kw 8760 Datenpunkte 

if input_user.heat_pump.exist:
    df['heat_pump'] = heat_pump(input_user.heat_pump.performance_kWh_year)

if input_user.ecar.exist:
  
    ladeleistung = 11 if input_user.ecar.wallbox else 2.7
    df['ecar'] = optimierte_ladesimulation(
        input_user.ecar.ziel_jahreskilometer,
        input_user.ecar.verbrauch_kwh_pro_100km, 
        ladeleistung).values # .values -> ignoriert Index
    
df.to_csv("test_df.csv", index=False)

if input_user.memory.exist:
    pass

# KWhJahr * Hausverbrauch + ele_car 

# kost konst 
# kost dynamisch
# diagramm 