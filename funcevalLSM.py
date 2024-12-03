import numpy as np
from funcderivation import func_derivation

def funcevalLSM(profile, settings):
    """
    Berechnet die Nahtparameterauswertung gemäß der Methode 'LSM'.

    Parameters:
        profile (np.ndarray): 2D-Array mit Profilpunkten (erste Spalte: x-Werte, zweite Spalte: y-Werte).
        settings (dict): Dictionary mit den Einstellungen, z.B. 'smoothparam', 'factor'.

    Returns:
        dict: Ergebnisse mit den Schlüsseln:
            - 'method': Verwendete Methode ('LSM').
            - 'DP_toe', 'DP_SP', 'DP_EP': Indizes für die relevanten Punkte.
            - 'radius': Radius des Kreises.
            - 'MP': Mittelpunkt des Kreises.
            - 'SP', 'EP': Start- und Endpunktkoordinaten.
            - 'maxdist': Maximale Abweichung zwischen Profil und Kreis.
    """
    results = {'method': 'LSM'}

    # Krümmung berechnen
    _, curvature = func_derivation(profile, settings['smoothparam'])

    # Schweißnahtpunkte bestimmen
    results['DP_toe'] = np.argmax(curvature[:, 1]) + 1  # +1 wegen Indexverschiebung

    results['DP_SP'] = results['DP_toe'] - (
        np.argmax(np.flipud(curvature[:results['DP_toe'] - 2, 1]) <= curvature[results['DP_toe'], 1] * settings['factor']) - 1
    )
    results['DP_EP'] = results['DP_toe'] + (
        np.argmax(curvature[results['DP_toe']:, 1] <= curvature[results['DP_toe'], 1] * settings['factor']) - 1
    )

    DP_toe_all = np.arange(results['DP_SP'], results['DP_EP'] + 1)

    # Nahtübergangsradius: Kleinste-Quadrate-Anpassung (analytische Lösung)
    A = np.ones((len(DP_toe_all), 3))
    A[:, 1] = profile[DP_toe_all, 0]
    A[:, 2] = profile[DP_toe_all, 1]
    D = profile[DP_toe_all, 0]**2 + profile[DP_toe_all, 1]**2
    c = np.linalg.lstsq(A, D, rcond=None)[0]

    MP_x = c[1] / 2
    MP_y = c[2] / 2

    results['radius'] = np.sqrt(c[0] + MP_x**2 + MP_y**2)

    # Koordinaten von Kreiszentrum, Start- und Endpunkt
    results['MP'] = [MP_x, MP_y]
    results['SP'] = profile[results['DP_SP'], :]
    results['EP'] = profile[results['DP_EP'], :]

    # Maximale Abweichung zwischen Profil und Kreis
    DP_MP_dist = np.sqrt(np.sum((results['MP'] - profile)**2, axis=1))
    results['maxdist'] = np.max(np.abs(DP_MP_dist[DP_toe_all] - results['radius']))

    return results
