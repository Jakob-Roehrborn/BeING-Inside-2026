import pandas as pd
from not_use.user_json import get_json_value

def load_data(csv_path, cols, separator=','):
    # 'sep' gibt an, welches Trennzeichen genutzt wird
    df = pd.read_csv(csv_path, usecols=cols, sep=separator)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    return df.sort_values('timestamp')

# --- ANWENDUNG ---
data_power = "strompreise_2026_sachsenenergie.csv"
data_heat_pump = 'f_d_h_2026.csv'

# 1. Die Strompreise (Komma-getrennt)
df_power = load_data(
    data_power, 
    ['timestamp', 'customer_price_gross_ct_per_kwh_konzession_1_32'], 
    separator=','
)

# 2. Die Wärmepumpe (Semikolon-getrennt)
df_heat_pump = load_data(
    data_heat_pump, 
    ['timestamp', 'f_d_h'], 
    separator=';'
)

# 3. Mergen (funktioniert jetzt, da beide DataFrames sauber geladen wurden)
df_combined = pd.merge(df_power, df_heat_pump, on='timestamp')

df_combined['total_value'] = (
    df_combined['customer_price_gross_ct_per_kwh_konzession_1_32'] * 
    df_combined['f_d_h']
)
gesamtsumme_fdh = df_combined['total_value'].sum()
print(f"Die Aufsummierung aller total_value Werte ergibt: {gesamtsumme_fdh}")

def heat_pump(value): # Wert kWh pro Jahr user Wärmepumpe, 
    return value * 33.714308790716046 # sum(f_d_h-Spalte*customer_price_gross_ct_per_kwh_konzession_1_32-Spalte)

print(heat_pump(get_json_value(["heat_pump", "performance_kWh"]))/100) 
    
#Optional: Als neue CSV speichern
#df_combined.to_csv("kombinierte_daten.csv", index=False)