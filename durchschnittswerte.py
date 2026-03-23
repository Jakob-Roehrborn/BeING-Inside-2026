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

# Durchschnittliches Profil mit 365 Tagen pro Jahr
df = df[~((df.index.month == 2) & (df.index.day == 29))]
df["dayofyear"] = df.index.dayofyear
profile = df.groupby("dayofyear")["tsun"].mean()


profile.to_frame().to_parquet("dresden_tsun_profile.parquet")

print(profile)
