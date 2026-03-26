import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd

def plot_auswertung(df, speicher_kap, input_user):
    print("Erstelle Graphen...")
    
    # 1. Echte Datetime-Achse erstellen, damit Matplotlib die Monate auf der X-Achse schön formatiert
    # Wir nehmen an, das Jahr ist 2025, passend zu deinem Timestamp in der main.py
    x_axis = pd.date_range(start="2025-01-01 00:00", periods=len(df), freq='h')
    
    # Figur mit 3 Untergraphen untereinander erstellen
    fig, axes = plt.subplots(3, 1, figsize=(12, 15))
    
    # GRAPH 1: Netzbezug vs. Einspeisung (kumuliert)
    axes[0].plot(x_axis, df['netz_bezug'].cumsum(), label='Kumulierter Netzbezug (kWh)', color='crimson', linewidth=2)
    axes[0].plot(x_axis, df['netz_einspeisung'].cumsum(), label='Kumulierte Einspeisung (kWh)', color='seagreen', linewidth=2)
    
    axes[0].set_title('Jahresbilanz: Strombezug vs. Einspeisung', fontsize=14)
    axes[0].set_ylabel('Energie (kWh)')
    axes[0].legend(loc='upper left')
    axes[0].grid(True, linestyle='--', alpha=0.6)

    # GRAPH 2: Kostenvergleich (Dynamisch vs. eprice)
    # Berechnung der Kosten für den konstanten Tarif
    # Formel: -Preis * Bezug + Vergütung * Einspeisung (Kosten sind negativ, Gewinn ist positiv)
    kosten_konstant = (-input_user.general_info.eprice * df['netz_bezug'] + 0.0778 * df['netz_einspeisung']).cumsum()
    kosten_dynamisch = df['ges_price'].cumsum()
    
    axes[1].plot(x_axis, kosten_dynamisch, label='Dynamischer Tarif', color='royalblue', linewidth=2)
    axes[1].plot(x_axis, kosten_konstant, label=f"Konstanter Tarif {input_user.general_info.eprice} ct/kWh", color='darkorange', linewidth=2, linestyle='--')
    
    axes[1].set_title('Kumulierte Stromkosten: Dynamisch vs. Konstant', fontsize=14)
    axes[1].set_ylabel('Kontostand (€)')
    axes[1].legend(loc='upper left')
    axes[1].grid(True, linestyle='--', alpha=0.6)


    # GRAPH 3: Speicherauslastung (Zoom auf einen Monat)
    if 'speicher_stand' in df.columns:
        # Hier ist die Linie etwas dicker (linewidth=1.5), da wir nun weniger Datenpunkte sehen
        axes[2].plot(x_axis, df['speicher_stand'], label='Stündlicher Speicherstand', color='purple', alpha=0.8, linewidth=1.5)
        axes[2].axhline(y=speicher_kap, color='red', linestyle='-', alpha=0.8, label=f'Max. Kapazität ({speicher_kap} kWh)')
        
        axes[2].set_title('Speicherauslastung im Juni (Detailansicht)', fontsize=14)
        axes[2].set_ylabel('Füllstand (kWh)')
        axes[2].set_ylim(0, speicher_kap * 1.1)
        axes[2].legend(loc='upper right')
    else:
        axes[2].text(0.5, 0.5, 'Kein Speicher vorhanden', ha='center', va='center', fontsize=14)
        axes[2].set_title('Speicherauslastung')
        axes[2].set_yticks([])

    axes[2].grid(True, linestyle='--', alpha=0.6)

    # X-ACHSE FORMATIEREN
    
    # Graph 1 & 2: Zeigen das ganze Jahr (Monate auf der X-Achse)
    for ax in axes[:2]:
        ax.xaxis.set_major_locator(mdates.MonthLocator())
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%b'))
        ax.set_xlim(x_axis[0], x_axis[-1])

    # Graph 3: Zeigt nur einen bestimmten Monat (z.B. Juni)
    zoom_start = pd.to_datetime("2025-06-01 00:00")
    zoom_ende = pd.to_datetime("2025-06-30 23:59")
    
    axes[2].set_xlim(zoom_start, zoom_ende)
    # Alle 3 Tage ein Datum anzeigen, sonst überlappt der Text
    axes[2].xaxis.set_major_locator(mdates.DayLocator(interval=3)) 
    axes[2].xaxis.set_major_formatter(mdates.DateFormatter('%d.%m.'))

    # Layout optimieren und speichern
    plt.tight_layout()
    plt.savefig("jahresauswertung_dashboard_presi.png", dpi=150)
    plt.close(fig)
    print("✅ Graphen gespeichert unter: jahresauswertung_dashboard.png")
    return