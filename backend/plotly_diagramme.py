import pandas as pd
import plotly.express as px
import numpy as np


def plot_cost(df, spalten, tage = 365, start_tag = 0, glättung_stunden = 24, title = 'Plott'):

    df = df.copy()
    df.index = pd.date_range(start="2024-01-01", periods=len(df), freq="h")
    
    start_zeit = df.index[0] + pd.Timedelta(days=start_tag)
    end_zeit = start_zeit + pd.Timedelta(days=tage)

    df_subset = df.loc[start_zeit:end_zeit].copy()

    if glättung_stunden > 1:
        # Mittelwert = mean
        df_subset = df_subset[spalten].resample(f"{glättung_stunden}h").mean()
    
    namen_mapping = {'kosten_konstant': 'Fixer Tarif', 'kosten_dynamisch': 'Dynamischer Tarif'}
    df_subset = df_subset.rename(columns=namen_mapping)
    plot_spalten = [namen_mapping.get(c, c) for c in spalten]

    fig = px.line(
        df_subset, 
        x=df_subset.index,  # Nutzt jetzt die echten Datums-Objekte
        y=plot_spalten,
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
                    yaxis_title = 'Kostenstand in Euro',
                    legend_title_text='Legende')
    
    fig.write_html(r"diagrams/cost_diagram.html", include_plotlyjs = 'directory') # 'cdn' benötigt Internet 
    return fig


def plot_grid_exchange(df, spalten, tage = 365, start_tag = 0, glättung_stunden = 24, title = 'Plott'):

    df = df.copy()
    df.index = pd.date_range(start="2024-01-01", periods=len(df), freq="h")
    
    start_zeit = df.index[0] + pd.Timedelta(days=start_tag)
    end_zeit = start_zeit + pd.Timedelta(days=tage)
    df_subset = df.loc[start_zeit:end_zeit].copy()

    if glättung_stunden > 1:
        df_subset = df_subset[spalten].resample(f"{glättung_stunden}h").mean()
    
    namen_mapping = {'netz_bezug': 'Netzbezug', 'netz_einspeisung': 'Netzeinspeisung'}
    df_subset = df_subset.rename(columns=namen_mapping)
    plot_spalten = [namen_mapping.get(c, c) for c in spalten]
    
    fig = px.line(
        df_subset, 
        x = df_subset.index,  # Nutzt jetzt die echten Datums-Objekte
        y = plot_spalten,
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
                    xaxis_title="Monat", 
                    yaxis_title = 'kWh',
                    legend_title_text='Legende')
    
    fig.write_html(r"diagrams/plot_grid_exchange.html", include_plotlyjs='directory') # 'cdn' benötigt Internet 
    return fig
#if __name__ == '__main__':

