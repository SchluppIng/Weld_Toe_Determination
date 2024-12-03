import numpy as np
from funcderivation import func_derivation

def funcevalangle(method, profile, settings, radiusresults):
    """
    Berechnet den Winkel basierend auf den Gradienten und der gewählten Methode.

    Parameters:
    method (str): Methode zur Berechnung des Winkels ('MAX' oder 'END').
    profile (np.ndarray): 2D-Array mit den Profilpunkten, wobei die erste Spalte x-Werte und die zweite Spalte y-Werte enthält.
    settings (dict): Dictionary mit den Einstellungen. Erwartet die Schlüssel:
                     - 'smoothparam': Glättungsparameter für die Ableitungsberechnung.
                     - 'smoothlen': Glättungslänge für die Mittelwertbildung.
    radiusresults (dict): Ergebnisse der Radiusberechnung, mit dem Schlüssel 'DP_EP' (Endpunkt-Index).

    Returns:
    dict: Ergebnisse mit folgenden Schlüsseln:
          - 'angle': Berechneter Winkel in Grad.
          - 'DP': Index des Datenpunkts, an dem der Winkel berechnet wurde.
          - 'sign': Vorzeichen des Gradienten am berechneten Punkt.
    """
    gradient, _ = func_derivation(profile, settings['smoothparam'])
    results = {}

    if method == 'MAX':
        if settings['smoothlen'] == 0:
            # Winkel basierend auf dem maximalen Gradienten
            max_grad = np.max(np.abs(gradient[:, 1]))
            results['angle'] = np.degrees(np.arctan(max_grad))
            results['DP'] = np.argmax(np.abs(gradient[:, 1]))
            results['sign'] = np.sign(gradient[results['DP'], 1])
        else:
            # Datenpunkt mit maximalem Gradienten
            DP = np.argmax(np.abs(gradient[:, 1]))
            DP_all = np.arange(DP + 1, len(profile))
            distances = np.cumsum(
                np.sqrt(np.diff(profile[DP_all, 0])**2 + np.diff(profile[DP_all, 1])**2)
            )
            DP_nr = np.searchsorted(distances, settings['smoothlen'])
            DP_nr = max(DP_nr, 5)  # Mindestens 5 Punkte verwenden

            # Gleitender Durchschnitt des Gradienten
            moving_avg = np.convolve(
                gradient[:, 1], np.ones(DP_nr) / DP_nr, mode='valid'
            )
            results['angle'] = np.degrees(np.arctan(np.max(np.abs(moving_avg))))
            results['DP'] = DP
            results['sign'] = np.sign(gradient[DP, 1])

    elif method == 'END':
        if settings['smoothlen'] == 0:
            # Winkel am Endpunkt (basierend auf Radius)
            results['angle'] = np.degrees(
                np.arctan(np.abs(gradient[radiusresults['DP_EP'] - 1, 1]))
            )
        else:
            # Punkte ab DP_EP sammeln
            DP_all = np.arange(radiusresults['DP_EP'], len(profile))
            distances = np.cumsum(
                np.sqrt(np.diff(profile[DP_all, 0])**2 + np.diff(profile[DP_all, 1])**2)
            )
            DP_nr = np.searchsorted(distances, settings['smoothlen'])

            if DP_nr > 0:
                DP_all = np.arange(
                    radiusresults['DP_EP'], radiusresults['DP_EP'] + DP_nr
                )
                # Lineare Regression für Glättung
                p = np.polyfit(profile[DP_all, 0], profile[DP_all, 1], 1)
                results['angle'] = np.abs(np.degrees(np.arctan(p[0])))
            else:
                results['angle'] = np.nan

        results['DP'] = radiusresults['DP_EP'] - 1
        results['sign'] = np.sign(gradient[results['DP'], 1])

    else:
        raise ValueError("Method does not exist")

    return results
