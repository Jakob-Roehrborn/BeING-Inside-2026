import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd

def plot_household_year(df):
    print('plotttttttttttttttttttttt')
    # 1. Vorbereitung: Zeitindex erstellen (8760 Stunden)
    df = df.copy()
    df.index = pd.date_range(start="2025-01-01", periods=len(df), freq="h")

    # 2. Glättung (Optional, aber empfohlen für das ganze Jahr)
    # Wir erstellen einen gleitenden Durchschnitt (Tagesmittelwert),
    # damit man vor lauter Zacken überhaupt noch etwas erkennt.
    df_smooth = df[['smart', 'nicht']].rolling(window=24*5, center=True).mean()

    # 3. Plot erstellen
    fig, ax = plt.subplots(figsize=(12, 6))

    # Linien zeichnen
    ax.plot(df_smooth.index, df_smooth['smart'], label='Verhalten: smart', color='royalblue', linewidth=1.5)
    ax.plot(df_smooth.index, df_smooth['nicht'], label='Verhalten: standart', color='orange', linewidth=1.5, alpha=0.8)

    # 4. X-Achse auf Monate formatieren
    ax.xaxis.set_major_locator(mdates.MonthLocator()) # Markierung jeden Monat
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b')) # Name des Monats (Jan, Feb...)

    # 5. Styling & Beschriftung
    ax.set_title('Auswirkung des Nutzerverhalten', fontsize=14, pad=15)
    ax.set_xlabel('Monat')
    ax.set_ylabel('Bilanz in Euro')
    ax.grid(True, linestyle='--', alpha=0.6)
    ax.legend(loc='upper right')

    # Layout optimieren und speichern
    plt.tight_layout()
    plt.savefig("diagrams/household_comparison.png", dpi=300) # Als Bild speichern
    plt.savefig("diagrams/household_comparison.png", dpi=300, bbox_inches='tight')

# Aufruf:
# plot_household_year(df)