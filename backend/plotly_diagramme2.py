# wichtig für png Generierung:  kaleido==0.2.1
# erstellt Diagramme als html, png in Ordner diagrams
# als png zeitaufwendig
# jeder plott eigene Funktion rolling_hours approx 24*7 Graphen schöner

import pandas as pd
import plotly.express as px
import plotly.io as pio

pio.kaleido.scope.default_format = "png" # wichtig png Erstellung viel schneller -> Engine wird nicht jedes mal neu gestartet

SCALE = 1

def plot_cost(df, columns, days = 365, start_day = 0, rolling_hours = 24, title = 'Plott', rolling = True, png = False):

    df = df.copy()
    df.index = pd.date_range(start="2025-01-01", periods=len(df), freq="h")
    
    start_zeit = df.index[0] + pd.Timedelta(days = start_day)
    end_zeit = start_zeit + pd.Timedelta(days = days)

    df_subset = df.loc[start_zeit:end_zeit].copy()

    if rolling_hours > 1:
        if rolling:
            df_subset[columns] = df_subset[columns].rolling(window=rolling_hours, center=True, min_periods=1).mean() # nähert die Punkte an, Anzahl bleibt gleich -> schönere Kurve
        else:
            df_subset[columns] = df_subset[columns].resample(f"{rolling_hours}h").mean() # Fasst Punkte zu einem Punkt = Mittelwert an
    
    namen_mapping = {'kosten_konstant': 'Fixer Tarif', 'kosten_dynamisch': 'Dynamischer Tarif'}
    df_subset = df_subset.rename(columns = namen_mapping)
    plot_columns = [namen_mapping.get(c, c) for c in columns]

    fig = px.line(
        df_subset, 
        x=df_subset.index, 
        y=plot_columns,
        title= title,
        template='plotly_white' #"plotly_dark" # Dunkel: cyborg Hell: plotly, plotly_white, ggplot2 Einfach: seaborn, none
    )

    fig.update_xaxes(
        dtick="M1",         # Zeige jeden 1. Monat 
        tickformat="%b",    # Format: "Jan", "Feb" %B -> für ausgeschrieben
        ticklabelmode="period"
    )

    # geht auch:
    # fig.update_layout(
    # plot_bgcolor="rgba(0,0,0,0)",  # Transparenter Hintergrund
    # paper_bgcolor="rgba(0,0,0,0)", # Transparenter Rand
    # font_color="#f0f0f0"           # Deine exakte Schriftfarbe
    # )

    fig.update_layout(hovermode="x unified", 
                    xaxis_title= "Monat", 
                    yaxis_title = 'Bilanz in Euro',
                    legend_title_text='Legende')
    
    fig.write_html(r"diagrams/cost_diagram.html", include_plotlyjs = 'directory') # 'cdn' benötigt Internet 
    if png:
        fig.write_image(r"diagrams/cost_diagram.png", scale= SCALE, width=1200, height=600) # wäre auch als pdf, svg möglich
    return fig

def plot_grid_exchange(df, columns, days = 365, start_day = 0, rolling_hours = 24, title = 'Plott', rolling = True, png = False):

    df = df.copy()
    df.index = pd.date_range(start= "2025-01-01", periods=len(df), freq="h")
    
    start_zeit = df.index[0] + pd.Timedelta(days=start_day)
    end_zeit = start_zeit + pd.Timedelta(days=days)
    df_subset = df.loc[start_zeit:end_zeit].copy()

    if rolling_hours > 1:
        if rolling:
            df_subset[columns] = df_subset[columns].rolling(window=rolling_hours, center=True, min_periods=1).mean() # nähert die Punkte an, Anzahl bleibt gleich -> schönere Kurve
        else:
            df_subset[columns] = df_subset[columns].resample(f"{rolling_hours}h").mean() # Fasst Punkte zu einem Punkt = Mittelwert an
    
    
    namen_mapping = {'netz_bezug': 'Netzbezug', 'netz_einspeisung': 'Netzeinspeisung'}
    df_subset = df_subset.rename(columns=namen_mapping)
    plot_columns = [namen_mapping.get(c, c) for c in columns]
    
    fig = px.line(
        df_subset, 
        x = df_subset.index,
        y = plot_columns,
        title= title,
        template='plotly_white' #"plotly_dark" # Dunkel: cyborg Hell: plotly, plotly_white, ggplot2 Einfach: seaborn, none
    )

    fig.update_xaxes(
        dtick="M1",         # Zeige jeden 1. Monat 
        tickformat="%b",    # Format: "Jan", "Feb" %B -> für ausgeschrieben
        ticklabelmode="period"
    )

    fig.update_layout(hovermode="x unified", 
                    xaxis_title="Monat", 
                    yaxis_title = 'kWh',
                    legend_title_text='Legende')
    
    fig.write_html(r"diagrams/plot_grid_exchange.html", include_plotlyjs='directory') # 'cdn' benötigt Internet 
    if png:
        fig.write_image(r"diagrams/plot_grid_exchange.png", scale=SCALE, width=1200, height=600)
    return fig

def plot_grid_exchange_cumsum(df, columns, days = 365, start_day = 0, rolling_hours = 24, title = 'Plott', rolling = True, png = False):

    df = df.copy()
    df.index = pd.date_range(start="2025-01-01", periods=len(df), freq="h")
    
    start_zeit = df.index[0] + pd.Timedelta(days=start_day)
    end_zeit = start_zeit + pd.Timedelta(days=days)
    df_subset = df.loc[start_zeit:end_zeit].copy()

    if rolling_hours > 1:
        if rolling:
            df_subset[columns] = df_subset[columns].rolling(window = rolling_hours, center = True, min_periods = 1).mean() # nähert die Punkte an, Anzahl bleibt gleich -> schönere Kurve
        else:
            df_subset[columns] = df_subset[columns].resample(f"{rolling_hours}h").mean() # Fasst Punkte zu einem Punkt = Mittelwert an
    
    
    namen_mapping = {'cumsum_netz_bezug': 'Netzbezug', 'cumsum_netz_einspeisung': 'Netzeinspeisung'}
    df_subset = df_subset.rename(columns=namen_mapping)
    plot_columns = [namen_mapping.get(c, c) for c in columns]
    
    fig = px.line(
        df_subset, 
        x = df_subset.index, 
        y = plot_columns,
        title= title,
        template='plotly_white' #"plotly_dark" # Dunkel: cyborg Hell: plotly, plotly_white, ggplot2 Einfach: seaborn, none
    )

    fig.update_xaxes(
        dtick="M1",         # Zeige jeden 1. Monat 
        tickformat="%b",    # Format: "Jan", "Feb" %B -> für ausgeschrieben
        ticklabelmode="period"
    )

    fig.update_layout(hovermode="x unified", 
                    xaxis_title="Monat", 
                    yaxis_title = 'kWh',
                    legend_title_text='Legende')
    
    fig.write_html(r"diagrams/plot_grid_exchange_cumsum.html", include_plotlyjs='directory') # 'cdn' benötigt Internet 
    if png:
        fig.write_image(r"diagrams/plot_grid_exchange_cumsum.png", scale=SCALE, width=1200, height=600)
    return fig

#if __name__ == '__main__':

