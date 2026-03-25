import matplotlib.pyplot as plt
import pandas as pd


def plot_data(df, columns_to_plot, title="Energieanalyse", 
              moving_avg_days=7, start_idx=0, end_idx=8760, 
              show_hourly=True):
    """
    Args:
        df: DataFrame mit Datetime-Index
        columns_to_plot: Liste von Spaltennamen
        title: Diagrammtitel
        moving_avg_days: Zeitspanne für den Trend
        start_idx: Startpunkt der Daten (0 bis 8760)
        end_idx: Endpunkt der Daten (0 bis 8760)
        show_hourly: Wenn False, wird nur der Moving Average geplottet
    """
    # 1. Datenbereich ausschneiden (Slicing)
    df_plot = df.iloc[start_idx:end_idx].copy()
    
    plt.figure(figsize=(15, 7))
    colors = ['#FFA500', '#1f77b4', '#2ca02c', '#d62728', '#9467bd']
    window = moving_avg_days * 24

    for i, col in enumerate(columns_to_plot):
        if col not in df_plot.columns:
            continue
            
        color = colors[i % len(colors)]
        
        # Originaldaten nur plotten, wenn erwünscht
        if show_hourly:
            plt.plot(df_plot.index, df_plot[col], color=color, alpha=0.3, 
                     linewidth=0.5, label=f"{col} (stündlich)")
        
        # Moving Average berechnen
        # Wir berechnen den MA auf dem ganzen DF, um Randeffekte beim Slicing zu vermeiden
        full_ma = df[col].rolling(window=window, center=True).mean()
        ma_to_plot = full_ma.iloc[start_idx:end_idx]
        
        plt.plot(df_plot.index, ma_to_plot, color=color, alpha=1.0, 
                 linewidth=2.5, label=f"{col} ({moving_avg_days}d-Trend)")

    # Design
    plt.title(f"{title} (Index {start_idx} bis {end_idx})", fontsize=16, fontweight='bold')
    plt.xlabel("Zeitverlauf", fontsize=12)
    plt.ylabel("Leistung (kW) / Energie", fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.legend(loc='upper right', frameon=True)
    plt.gcf().autofmt_xdate() 
    
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    # plot_energy_data(df, ['solar', 'heat_pump', 'ecar'], title="PV-Erzeugung vs. Verbraucher")
    csv_path = r'backend\solar_base\solar_base_01099_2020_2025.csv'
    df = pd.read_csv(csv_path)
    plot_data(df, ['temp_mean'], moving_avg_days=2, show_hourly = False)