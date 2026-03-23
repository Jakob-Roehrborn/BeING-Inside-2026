import meteostat as ms
import pandas as pd
from datetime import date

POINT = ms.Point(51.0504, 13.7373, 113)  # Dresden
START = date(2005, 1, 1)
END = date(2025, 1, 1)

# Stationen in der Nähe
stations = ms.stations.nearby(POINT, limit=3)

# Tagesdaten abrufen
ts = ms.daily(stations, START, END)
df = ms.interpolate(ts, POINT).fetch()

# Kalendertag extrahieren
df["dayofyear"] = df.index.dayofyear

# Durchschnittliches Profil
profile = df.groupby("dayofyear")["tsun"].mean()

print(profile)
