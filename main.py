from user_json import update_config_from_api, get_json_value, get_coordinates_from_user, get_ecar_from_user
from solar_base import generate_weather_master
from solar_calculation import main_kwp_performance
from heat_pump import heat_pump
from eauto import optimierte_ladesimulation
from haushalt_csv import household

import pandas as pd

def timestamp():
    start_date = "2025-01-01 00:00:00"
    end_date = "2025-12-31 23:00:00"
    full_year = pd.date_range(start=start_date, end=end_date, freq='h')
    formatted_timestamps = full_year.strftime('%m-%d %H:00')
    
    return formatted_timestamps

update_config_from_api('user.json')

lat, lon, plz = get_coordinates_from_user()

df = pd.DataFrame()
df['timestamp'] = timestamp()

number_of_person = get_json_value(['general_info', "number_of_person"])
total_consumption = get_json_value(['general_info', "total_consumption"])
df['household'] = household(total_consumption, number_of_person)/1000

if get_json_value(["solar_system","exist"]):
    generate_weather_master(lat, lon, plz)
    df['solar'] = main_kwp_performance(lat, lon, plz) # df mit Spalten: mm_dd_hh, performance_kw 8760 Datenpunkte 
    #solar_df.to_csv("test_solar.csv", index=False)

if get_json_value(["heat_pump","exist"]):
    df['heat_pump'] = heat_pump()
    #heat_pump = get_json_value(["heat_pump", "performance_kWh"]) * 33.714308790716046 /100
    #heat_pump_df.to_csv("test_heat_pump.csv", index=False)

if get_json_value(["ecar","exist"]):
    resutlt = get_ecar_from_user('user.json')
    df['ecar'] = optimierte_ladesimulation(*resutlt).values # .values -> ignoriert Index
    
df.to_csv("test_df.csv", index=False)
if get_json_value(["memory","exist"]):
    pass

# KWhJahr * Hausverbrauch + ele_car 