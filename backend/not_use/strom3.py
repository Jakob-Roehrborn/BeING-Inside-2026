import pandas as pd

def load_data(csv_path, cols, separator=','):
    # 'sep' gibt an, welches Trennzeichen genutzt wird
    df = pd.read_csv(csv_path, usecols=cols, sep=separator)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    return df.sort_values('timestamp')

def get_price_by_timestamp(csv_file, target_timestamp, column_name='customer_price_gross_ct_per_kwh_konzession_1_32'):
    """
    Liest den Brutto-Kundenpreis für einen spezifischen Zeitstempel aus einer CSV.
    """
    try:
        df = load_data(
            csv_file, 
            ['timestamp', 'customer_price_gross_ct_per_kwh_konzession_1_32'], 
            separator=','
        )

        target_dt = pd.to_datetime(target_timestamp)
        
        result = df[df['timestamp'] == target_dt]
        
        if not result.empty:
            return result.iloc[0][column_name]
        else:
            print(f"Zeitstempel {target_timestamp} nicht in der Datei gefunden.")
            return None
    except Exception as e:
        print(f"Fehler beim Lesen der CSV: {e}")
        return None
    
# --- Beispielaufruf ---
price = get_price_by_timestamp(r'material\strompreise_2026_sachsenenergie.csv', '2026-01-01 00:00:00')
if price:
    print(f"Der Preis ist: {price} ct/kWh")
    
def get_price_sequentially(csv_file, column_name='customer_price_gross_ct_per_kwh_konzession_1_32'):
    """
    Erstellt einen Generator, der bei jedem Aufruf den nächsten Preis liefert.
    """
    df = pd.read_csv(csv_file, usecols=[column_name], sep=',')
    
    for price in df[column_name]:
        yield price
price_gen = get_price_sequentially(r'material\strompreise_2026_sachsenenergie.csv')

# 2. Den jeweils nächsten Wert abholen
print(next(price_gen)) # Wert 1 (00:00:00)
print(next(price_gen)) # Wert 2 (01:00:00)
print(next(price_gen)) # Wert 3 (02:00:00)

def load_price_list(csv_file, column_name='customer_price_gross_ct_per_kwh_konzession_1_32'):
    """
    Lädt die gesamte Spalte in eine Liste für schnellen Index-Zugriff.
    """
    df = pd.read_csv(csv_file, usecols=[column_name], sep=',')
    return df[column_name].tolist()

# --- Anwendung ---
prices = load_price_list(r'material\strompreise_2026_sachsenenergie.csv')

# Zugriff über den Index [0 = erste Zeile, 1 = zweite Zeile, ...]
print(f"Erster Wert: {prices[0]}")
print(f"Zehnter Wert: {prices[9]}")









