import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def simuliere_e_auto_mit_soc(kapazitaet_kwh, laufleistung_jahr_km, verbrauch_100km, max_ladeleistung_kw, start_ladezeit, anteil_zu_Hause):
    start_datum = datetime(2024, 1, 1)
    stunden_jahr = 8760
    zeitstempel = [start_datum + timedelta(hours=i) for i in range(stunden_jahr)]
    
    last_profil = np.zeros(stunden_jahr)
    
    # Startzustand: Batterie ist zu Beginn voll
    aktueller_soc_kwh = kapazitaet_kwh

    laufleistung_jahr_km = laufleistung_jahr_km*anteil_zu_Hause
    
    # Tägliche Kilometer generieren (wie gehabt)
    np.random.seed(42)
    tages_kilometer = np.random.normal(laufleistung_jahr_km/365, (laufleistung_jahr_km/365) * 0.2, 365)
    tages_kilometer = np.maximum(tages_kilometer, 0)
    tages_kilometer = tages_kilometer * (laufleistung_jahr_km / tages_kilometer.sum())
    
    for tag in range(365):
        # 1. VERBRAUCH: Das Auto fährt (wir ziehen die Energie vom SoC ab)
        energie_verbrauch_tag = (tages_kilometer[tag] / 100) * verbrauch_100km
        aktueller_soc_kwh -= energie_verbrauch_tag
        
        # Sicherheitscheck: SoC kann nicht unter 0 sinken
        aktueller_soc_kwh = max(0, aktueller_soc_kwh)
        
        # 2. LADEN: Start um 19:00 Uhr
        start_stunde_index = tag * 24 + start_ladezeit
        
        # Wir laden nur so viel, wie bis zur Maximalkapazität fehlt
        lade_bedarf = kapazitaet_kwh - aktueller_soc_kwh
        
        aktuelle_stunde = start_stunde_index
        while lade_bedarf > 0.001 and aktuelle_stunde < stunden_jahr:
            # Wir laden entweder mit max. Leistung oder nur das, was noch in die Batterie passt
            leistung_in_dieser_stunde = min(max_ladeleistung_kw, lade_bedarf)
            
            last_profil[aktuelle_stunde] = leistung_in_dieser_stunde
            aktueller_soc_kwh += leistung_in_dieser_stunde
            lade_bedarf -= leistung_in_dieser_stunde
            aktuelle_stunde += 1
            
    df = pd.DataFrame({
        'Ladeleistung_kW': last_profil
    })
    
    return df

# Beispielaufruf
