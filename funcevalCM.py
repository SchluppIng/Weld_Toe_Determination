import numpy as np
from funcderivation import func_derivation

def funcevalCM(profile, settings):
    """
    Berechnet Nahtparameterauswertung gemäß der Methode 'CM'.

    Parameters:
    profile (np.ndarray): 2D-Array mit den Profilpunkten, wobei die erste Spalte x-Werte und die zweite Spalte y-Werte enthält.
    settings (dict): Dictionary mit den Einstellungen, erwartet einen Schlüssel 'smoothparam'.

    Returns:
    dict: Ergebnisse mit folgenden Schlüsseln:
          - 'method': Verwendete Methode ('CM').
          - 'radius': Radius des Kreises am Nahtübergang.
          - 'DP_toe': Index des Punktes mit maximaler Krümmung.
          - 'SP': Koordinaten des Punktes mit maximaler Krümmung.
          - 'MP': Koordinaten des Kreismittelpunkts.
          - 'maxdist': Maximale Abweichung zwischen Profil und Kreis.
    """
    results = {'method': 'CM'}

    # Gradient und Krümmung berechnen
    gradient, curvature = func_derivation(profile, settings['smoothparam'])
    profile = profile[1:-1, :]  # Profile kürzen, damit es zu curvature und gradient passt

    # Radius als Kehrwert der maximalen Krümmung
    max_curvature = np.max(curvature[:, 1])
    results['radius'] = 1 / max_curvature if max_curvature != 0 else np.inf

    # Punkt mit maximaler Krümmung finden
    results['DP_toe'] = np.argmax(curvature[:, 1])

    # Normalisierter Normalenvektor am Punkt mit maximaler Krümmung
    normalv = np.array([-gradient[results['DP_toe'], 1], 1])
    normalv /= np.linalg.norm(normalv)

    # Schweißnahtpunkt (SP) und Kreismittelpunkt (MP)
    results['SP'] = profile[results['DP_toe'], :]
    results['MP'] = results['SP'] + normalv * results['radius']

    # Maximale Abweichung zwischen Profil und Kreis
    DP_MP_dist = np.sqrt(np.sum((results['MP'] - profile) ** 2, axis=1))
    dp_start = np.where(DP_MP_dist <= results['radius'])[0][0]
    dp_end = np.where(DP_MP_dist <= results['radius'])[0][-1]

    if dp_start is not None and dp_end is not None:
        results['maxdist'] = np.max(np.abs(DP_MP_dist[dp_start:dp_end] - results['radius']))
    else:
        results['maxdist'] = np.nan  # Kein gültiger Bereich gefunden

    return results
