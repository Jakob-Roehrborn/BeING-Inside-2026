# Achtung mit kWh und Wh!!!
# Personenanzahl wird aktuell nicht beachtet - Frontend

import pandas as pd

def household():
    input_file = r'material\synPRO_el_family.dat'
    df = pd.read_csv(input_file, sep=';', comment='#')
    df['datetime'] = pd.to_datetime(df['unixtimestamp'], unit='s')
    df.set_index('datetime', inplace=True)

    hourly_df = df['P_el'].resample('1h').mean().reset_index()
    hourly_df['P_el_Wh'] = hourly_df['P_el'].round(2)
    hourly_df = hourly_df.drop(columns=['P_el'])

    #hourly_df.to_csv(output_file_basis, index=False)

    ist_jahresverbrauch_wh = hourly_df['P_el_Wh'].sum()

    norm_df = hourly_df[['datetime']].copy()
    anteil = hourly_df['P_el_Wh'] / ist_jahresverbrauch_wh
    norm_df['P_el_anteil_gesamt'] = anteil.round(7)
    #norm_df['P_el_pro_person_normiert_Wh'] = (norm_df['P_el_normiert_Wh'] / personen_anzahl).round(2)

    #norm_df.to_csv('Household.csv', index=False)
    return norm_df[['P_el_anteil_gesamt']]

    # norm_df.to_csv(output_file_normiert, index=False)
    # print(f"-> 2. Normierte Tabelle (skaliert auf {ziel_jahresverbrauch_kwh} kWh) erfolgreich erstellt!")
    # print(f"Kontrolle: Summe der normierten Daten beträgt {(norm_df['P_el_normiert_Wh'].sum() / 1000):.2f} kWh")


# ---------------------------------------------------------
# Einstellungen anpassen
# ---------------------------------------------------------
# input_file = 'synPRO_el_family.dat'
# output_file_basis = 'hourly_el_family_basis.csv'
# output_file_normiert = 'hourly_el_family_normiert.csv'

# # Hier den gewünschten Jahresverbrauch (in kWh) eintragen:
# ziel_jahresverbrauch_kwh = 3000
# personen_anzahl = 4

# ---------------------------------------------------------
# 1. Daten einlesen & vorbereiten
# ---------------------------------------------------------
# df = pd.read_csv(input_file, sep=';', comment='#')

# Zeitstempel umwandeln und als Index setzen
# df['datetime'] = pd.to_datetime(df['unixtimestamp'], unit='s')
# df.set_index('datetime', inplace=True)

# # ---------------------------------------------------------
# # 2. BASIS-Tabelle erstellen & abspeichern
# # ---------------------------------------------------------
# # Wir nehmen den Mittelwert, um aus 15-Min-Leistungswerten (W) die Stundenenergie (Wh) zu erhalten
# hourly_df = df['P_el'].resample('1h').mean().reset_index()

# # Spalte für bessere Lesbarkeit in Wattstunden (Wh) umbenennen und runden
# hourly_df['P_el_Wh'] = hourly_df['P_el'].round(2)
# hourly_df = hourly_df.drop(columns=['P_el'])

# # Erste Datei speichern
# hourly_df.to_csv(output_file_basis, index=False)
# print("-> 1. Basis-Tabelle erfolgreich erstellt!")


# ---------------------------------------------------------
# 3. NORMIERTE Tabelle erstellen & abspeichern
# ---------------------------------------------------------
# Den echten Verbrauch aus den Daten als Basis berechnen
# ist_jahresverbrauch_wh = hourly_df['P_el_Wh'].sum()

# # Den gewünschten Zielverbrauch in Wattstunden (Wh) umrechnen
# ziel_jahresverbrauch_wh = ziel_jahresverbrauch_kwh * 1000

# # Neue Tabelle anlegen (wir kopieren nur die Zeit-Spalte)
# norm_df = hourly_df[['datetime']].copy()

# # A) Anteil dieser speziellen Stunde am gesamten echten Jahresverbrauch
# anteil = hourly_df['P_el_Wh'] / ist_jahresverbrauch_wh
# norm_df['P_el_anteil_gesamt'] = anteil.round(7)

# B) Auf den Zielverbrauch skalierter Stundenverbrauch (Wh)
# norm_df['P_el_normiert_Wh'] = (anteil * ziel_jahresverbrauch_wh).round(2)

# # C) Normierter Stundenverbrauch pro Person (Wh)
# norm_df['P_el_pro_person_normiert_Wh'] = (norm_df['P_el_normiert_Wh'] / personen_anzahl).round(2)

# # Zweite Datei speichern
# norm_df.to_csv(output_file_normiert, index=False)
# print(f"-> 2. Normierte Tabelle (skaliert auf {ziel_jahresverbrauch_kwh} kWh) erfolgreich erstellt!")

# # Kurze Kontrolle zur Sicherheit:
# print(f"Kontrolle: Summe der normierten Daten beträgt {(norm_df['P_el_normiert_Wh'].sum() / 1000):.2f} kWh")