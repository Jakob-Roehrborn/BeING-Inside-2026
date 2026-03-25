import matplotlib.pyplot as plt
import pandas as pd


def plot_data(df, columns_to_plot, title="Plott", moving_avg_days=7):
    """
    Plottet beliebige Spalten eines DataFrames gegen den Index.
    
    Args:
        df: DataFrame mit Datetime-Index
        columns_to_plot: Liste von Spaltennamen, z.B. ['solar', 'heat_pump']
        title: Diagrammtitel
        moving_avg_days: Zeitspanne für den gleitenden Durchschnitt (Trendlinie)
    """
    plt.figure(figsize=(15, 7))
    
    # Standard-Farben für Konsistenz
    colors = ['#FFA500', '#1f77b4', '#2ca02c', '#d62728', '#9467bd'] # Orange, Blau, Grün, Rot, Lila
    
    # Fenstergröße für Durchschnitt (Tage * 24h)
    window = moving_avg_days * 24

    for i, col in enumerate(columns_to_plot):
        if col not in df.columns:
            print(f"Warnung: Spalte '{col}' nicht im DataFrame gefunden.")
            continue
            
        color = colors[i % len(colors)]
        
        # 1. Die originalen stündlichen Daten (blasser/dünner)
        plt.plot(df.index, df[col], color=color, alpha=0.3, linewidth=0.5, label=f"{col} (stündlich)")
        
        # 2. Den gleitenden Durchschnitt (Trendlinie)
        ma_col = df[col].rolling(window=window, center=True).mean()
        plt.plot(df.index, ma_col, color=color, alpha=1.0, linewidth=2, label=f"{col} ({moving_avg_days}d-Trend)")

    # Design & Beschriftung
    plt.title(title, fontsize=16, fontweight='bold')
    plt.xlabel("Zeitverlauf (Monate)", fontsize=12)
    plt.ylabel("Leistung (kW) / Energie", fontsize=12)
    plt.grid(True, which='both', linestyle='--', alpha=0.5)
    plt.legend(loc='upper right', frameon=True, shadow=True)
    
    # X-Achse automatisch schön formatieren (Monatsnamen)
    plt.gcf().autofmt_xdate() 
    
    plt.tight_layout()
    plt.show()

if __name__ == "__manin__":
    # plot_energy_data(df, ['solar', 'heat_pump', 'ecar'], title="PV-Erzeugung vs. Verbraucher")
    csv_path = r"solar_base\solar_base_01099_2020_2025.csv"
    df = pd.read_csv(csv_path)
    plot_data(df, ['temp_mean'])