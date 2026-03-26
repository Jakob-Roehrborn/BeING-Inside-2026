import pandas as pd

def read_price_data(csv_path, start_time=None, end_time=None):
    # 1. Nur die benötigten Spalten laden 
    cols = ['timestamp', 'customer_price_gross_ct_per_kwh_konzession_1_32']
    df = pd.read_csv(csv_path, usecols=cols)

    # 2. Timestamp in echte Datetime-Objekte umwandeln
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    
    # 3. Sortieren
    df = df.sort_values('timestamp')

    # 4. Filtern nach Zeitspanne
    if start_time and end_time:
        start = pd.to_datetime(start_time)
        end = pd.to_datetime(end_time)
        mask = (df['timestamp'] >= start) & (df['timestamp'] <= end)
        return df.loc[mask]
    
    return df

def heat_pump(csv_path, start_time=None, end_time=None):
    # 1. Nur die benötigten Spalten laden 
    cols = ['timestamp', 'f_d_h']
    df = pd.read_csv(csv_path, usecols=cols)

    # 2. Timestamp in echte Datetime-Objekte umwandeln
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    
    # 3. Sortieren
    df = df.sort_values('timestamp')

    # 4. Filtern nach Zeitspanne
    if start_time and end_time:
        start = pd.to_datetime(start_time)
        end = pd.to_datetime(end_time)
        mask = (df['timestamp'] >= start) & (df['timestamp'] <= end)
        return df.loc[mask]
    
    return df

# --- ANWENDUNG ---
data_power = "strompreise_2026_sachsenenergie.csv"
data_heat_pump = 'f_d_h_2026.csv'

df_power = read_price_data(data_power)
df_heat_pump = heat_pump(data_heat_pump)

# 1. Die beiden DataFrames mergen (zusammenführen)
# 'on="timestamp"' sorgt dafür, dass nur Zeilen mit gleicher Zeit kombiniert werden
df_combined = pd.merge(df_power, df_heat_pump, on='timestamp')

# 2. Eine neue Spalte mit der Summe erstellen
# Achtung: Achte darauf, ob die Einheiten (ct/kWh vs. ?) zusammenpassen!
df_combined['total_value'] = (
    df_combined['customer_price_gross_ct_per_kwh_konzession_1_32'] * 
    df_combined['f_d_h']
)

# 3. Das Ergebnis anschauen
print(df_combined[['timestamp', 'total_value']].head())

#Optional: Als neue CSV speichern
df_combined.to_csv("kombinierte_daten.csv", index=False)




# customer_price_kWh = read_price_data(
#     DATEI, 
#     start_time="2026-01-01 00:00:00", 
#     end_time="2026-03-30 00:00:00"
# )

#print(customer_price_kWh)

# Einzelwert abfragen: Was kostet der Strom am 01.03. um 12:00?
# Wir suchen den exakten Zeitstempel
# suche = pd.to_datetime("2026-03-01 00:00:00")
# einzelwert = customer_price_kWh[customer_price_kWh['timestamp'] == suche]

# if not einzelwert.empty:
#     preis = einzelwert['customer_price_gross_ct_per_kwh_konzession_1_32'].iloc[0]
#     print(f"\nPreis am {suche}: {preis} ct/kWh")