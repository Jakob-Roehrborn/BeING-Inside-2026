# Achtung mit kWh und Wh!!!
# Personenanzahl wird aktuell nicht beachtet - Frontend
# smart = True -> Ersparnis ca. 1.2379444826204349€

import pandas as pd

def household(smart = False):   
    input_file = r'./material/hausehold_smart.csv' if smart else r'./material/hausehold_normal.csv'
    df = pd.read_csv(input_file, sep=',', comment='#')
    return df[['return_value']]

# ==== Alte =====
def household_old(smart = False):   

    if smart:
        input_file = r'./material/household_smart_only.csv'
        #input_file = r'material/hourly_el_family.csv'
        df = pd.read_csv(input_file, sep=',', comment='#')
        ist_jahresverbrauch = df['P_el'].sum()
        df['return_value'] = df['P_el'] / ist_jahresverbrauch
        df.to_csv('hausehold_smart.csv',index=False)
        return df[['return_value']]
    else:
        input_file = r'material/synPRO_el_family.dat'
        df = pd.read_csv(input_file, sep=';', comment='#')
        df['datetime'] = pd.to_datetime(df['unixtimestamp'], unit='s')
        df.set_index('datetime', inplace=True)

        hourly_df = df['P_el'].resample('1h').mean().reset_index()
        hourly_df['P_el_Wh'] = hourly_df['P_el'].round(2)
        hourly_df = hourly_df.drop(columns=['P_el'])
        norm_df = hourly_df[['datetime']].copy()
        ist_jahresverbrauch_wh = hourly_df['P_el_Wh'].sum()
        anteil = hourly_df['P_el_Wh'] / ist_jahresverbrauch_wh
        norm_df['P_el_anteil_gesamt'] = anteil.round(7)
    return norm_df[['P_el_anteil_gesamt']]

    # norm_df.to_csv(output_file_normiert, index=False)
    # print(f"-> 2. Normierte Tabelle (skaliert auf {ziel_jahresverbrauch_kwh} kWh) erfolgreich erstellt!")
    # print(f"Kontrolle: Summe der normierten Daten beträgt {(norm_df['P_el_normiert_Wh'].sum() / 1000):.2f} kWh")