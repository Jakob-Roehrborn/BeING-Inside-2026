import pandas as pd
import numpy as np
import random
import matplotlib.pyplot as plt
import time

# max_leistung_kw mit Wallbox 11.0 ohne 2.7


def optimierte_ladesimulation(
        ziel_jahreskilometer = 15000,
        verbrauch_kwh_pro_100km = 18.0,
        max_leistung_kw = 11.0):
    
    input_filepath = r'material\synPRO_emob_row_1_hh_1_ev_id_1_2Ay3060_high_urban_1_charging_1_flex.dat'
    
    start_time = time.time()  # Für die Laufzeitmessung
    #print("Starte optimierte Datenverarbeitung...")

    # 1. Metadaten-Header überspringen
    skip_lines = 0
    with open(input_filepath, 'r', encoding='utf-8') as f:
        for line in f:
            if line.startswith('YYYYMMDD'): break
            skip_lines += 1

    # 2. Einlesen (OPTIMIERT: Nur notwendige Spalten laden)
    df = pd.read_csv(
        input_filepath,
        sep=';',
        skiprows=skip_lines,
        usecols=['YYYYMMDD', 'hhmmss', 'P_charger_grid_kW']
    )

    # 3. Schnelle Datums-Konvertierung
    df['datetime'] = pd.to_datetime(
        df['YYYYMMDD'].astype(str) + df['hhmmss'].astype(str).str.zfill(6),
        format='%Y%m%d%H%M%S'
    )
    df.set_index('datetime', inplace=True)
    df['P_charger_grid_kW'] = pd.to_numeric(df['P_charger_grid_kW'], errors='coerce')

    # 4. Aggregation auf Stunden
    df_hourly = df['P_charger_grid_kW'].resample('1h').mean()

    # 5. Profile extrahieren (OPTIMIERT: Speichern als reine Numpy-Arrays)
    jan_days = {i: [] for i in range(7)}
    for date, group in df_hourly.groupby(df_hourly.index.date):
        if len(group) == 24:
            jan_days[date.weekday()].append(group.values)

    # Falls an einem Wochentag keine Daten vorliegen, leeres Profil anlegen
    profiles = {w: (np.array(v) if len(v) > 0 else np.zeros((1, 24))) for w, v in jan_days.items()}

    # 6. Jahresdaten generieren (OPTIMIERT: Vektorisiert via Numpy statt while-Schleife)
    np.random.seed(42)
    days_in_year = pd.date_range('2021-01-01', '2021-12-31', freq='D')

    # Vorab-Allokation eines Arrays für das ganze Jahr (365 Tage * 24 h = 8760)
    full_year_data = np.zeros(len(days_in_year) * 24)

    for i, day in enumerate(days_in_year):
        wd = day.weekday()
        profs = profiles[wd]
        chosen_profile = profs[np.random.randint(0, len(profs))]  # Zieht Zufalls-Tagesprofil
        # 24 Stunden-Block in das Jahres-Array kopieren
        full_year_data[i * 24: (i + 1) * 24] = chosen_profile

    # 7. Normierung auf Kilometerleistung (OPTIMIERT: Mathematische Skalar-Multiplikation)
    gesamtenergie = full_year_data.sum()
    ziel_energie = ziel_jahreskilometer * (verbrauch_kwh_pro_100km / 100.0)

    if gesamtenergie > 0:
        # Multipliziert in Millisekunden alle 8760 Werte mit dem Faktor
        full_year_data *= (ziel_energie / gesamtenergie)

    # 8. Leistungs-Kappung & Spillover (OPTIMIERT: Schneller Array-Durchlauf)
    capped_data = np.empty_like(full_year_data)  # Leeres Array vorbereiten
    ueberschuss = 0.0

    for i in range(len(full_year_data)):
        aktueller_bedarf = full_year_data[i] + ueberschuss
        if aktueller_bedarf > max_leistung_kw:
            capped_data[i] = max_leistung_kw
            ueberschuss = aktueller_bedarf - max_leistung_kw
        else:
            capped_data[i] = aktueller_bedarf
            ueberschuss = 0.0

    # 9. Ergebnis-DataFrame erstellen
    full_year_idx = pd.date_range('2021-01-01', '2021-12-31 23:00:00', freq='1h')
    df_res = pd.DataFrame({'Ladeleistung_kW': np.round(capped_data, 4)}, index=full_year_idx)

    return df_res[['Ladeleistung_kW']]

    # Speichern
    # df_res.to_csv(output_filepath, sep=';', index=True, index_label='datetime')

    # end_time = time.time()
    # print(f"✅ CSV erfolgreich erstellt in {end_time - start_time:.4f} Sekunden!")
    # print(f"Gesamtenergie im System: {df_res['Ladeleistung_kW'].sum():.2f} kWh\n")

def plott(df_res, output_filepath, ziel_jahreskilometer, max_leistung_kw):
    # ==========================
    # --- OPTIONAL: PLOTTING ---
    # ==========================
    print("Erstelle Graphen...")
    plot_filename = output_filepath.replace('.csv', '.png')

    # Gleitender 7-Tage-Durchschnitt für die Trendlinie
    df_res['Trend_7Tage'] = df_res['Ladeleistung_kW'].rolling(window=168, min_periods=1).mean()

    fig, ax = plt.subplots(figsize=(15, 6))
    ax.plot(df_res.index, df_res['Ladeleistung_kW'], color='royalblue', alpha=0.5, linewidth=0.5,
            label='Stündliche Ladeleistung (kW)')
    ax.plot(df_res.index, df_res['Trend_7Tage'], color='darkorange', linewidth=2, label='7-Tage Trend')

    ax.set_title(f'Jahres-Ladekurve ({ziel_jahreskilometer} km | Max. {max_leistung_kw} kW)', fontsize=14)
    ax.set_xlabel('Datum', fontsize=12)
    ax.set_ylabel('Ladeleistung (kW)', fontsize=12)
    ax.set_ylim(0, max_leistung_kw * 1.1)
    ax.grid(True, linestyle='--', alpha=0.6)
    ax.legend(loc='upper right')

    fig.tight_layout()
    fig.savefig(plot_filename, dpi=150)
    plt.close(fig)
    print(f"✅ Graph gespeichert unter: {plot_filename}")


# --- AUSFÜHRUNG ---
# input_file = r'material\synPRO_emob_row_1_hh_1_ev_id_1_2Ay3060_high_urban_1_charging_1_flex.dat'
# output_file = 'ladesimulation_optimiert.csv'

# print(optimierte_ladesimulation(
#     ziel_jahreskilometer = 15000,
#     verbrauch_kwh_pro_100km = 18.0,
#     max_leistung_kw = 2.7
# ))