import pandas as pd

def load_data(csv_path, cols, separator=','):
    df = pd.read_csv(csv_path, usecols=cols, sep=separator)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    return df.sort_values('timestamp')

def heat_pump(performance_kWh_year):

    data_path = r'material\f_d_h_2026.csv'

    df = load_data(
        data_path, 
        ['timestamp', 'f_d_h'], 
        separator=';'
    )
    df['heat_pump'] = df['f_d_h'] * performance_kWh_year
    return df[['heat_pump']] # 'timestamp'