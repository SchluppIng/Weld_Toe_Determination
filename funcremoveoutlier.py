import numpy as np
import pandas as pd

def funcremoveoutlier(profile, settings):
    if settings['outliermethod'] == 'remove':
        # Verwenden von Pandas zur Entfernung von Ausreißern mittels gleitendem Median
        df = pd.DataFrame(profile, columns=['x', 'y'])
        df['y'] = df['y'].rolling(window=3, center=True).median()  # Verwenden von gleitendem Median mit Fenstergröße 3
        mask = df['y'].notna()  # Maske für nicht-NaN-Werte
        profile_new = df[mask].values  # Nur die Werte ohne NaN zurückgeben
    elif settings['outliermethod'] == 'none':
        profile_new = profile
    else:
        raise ValueError('Unknown removemode')
    return profile_new