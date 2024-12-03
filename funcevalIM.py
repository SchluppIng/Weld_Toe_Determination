import numpy as np
from funcderivation import func_derivation

def funcevalIM(profile, settings):
    """
    Berechnet Nahtparameterauswertung gemäß der Methode 'IM'.

    Parameters:
    profile (np.ndarray): 2D-Array mit den Profilpunkten, wobei die erste Spalte x-Werte und die zweite Spalte y-Werte enthält.
    settings (dict): Dictionary mit den Einstellungen. Erwartet die Schlüssel:
                     - 'smoothparam': Glättungsparameter für die Krümmungsberechnung.
                     - 'crit1', 'crit2', 'crit3': Kriterien für die Bewertung.

    Returns:
    dict: Ergebnisse mit folgenden Schlüsseln:
          - 'method': Verwendete Methode ('IM').
          - 'radius': Radius des Kreises am Nahtübergang.
          - 'MP': Koordinaten des Kreismittelpunkts.
          - 'SP': Koordinaten des Startpunkts.
          - 'EP': Koordinaten des Endpunkts.
          - 'maxdist': Maximale Abweichung zwischen Profil und Kreis.
          - 'DP_SP': Index des Startpunkts.
          - 'DP_EP': Index des Endpunkts.
    """
    results = {
        'method': 'IM',
        'radius': np.nan,
        'MP': [np.nan, np.nan],
        'SP': [np.nan, np.nan],
        'EP': [np.nan, np.nan],
        'maxdist': np.nan,
        'DP_SP': np.nan,
        'DP_EP': np.nan
    }

    # Einstellungen für den Radius
    radius_min = 0.01
    radius_max = 10.0
    radius_delta = 0.01

    # Delta für die x-Distanz
    delta_x_notch = 2.0

    # Krümmung berechnen
    _, curvature = func_derivation(profile, settings['smoothparam'])

    # Punkt mit maximaler Krümmung finden
    DP_toe = np.argmax(curvature[:, 1] >= max(curvature[:, 1]) * 0.9) + 1

    # Bereich für mögliche Startpunkte (SP)
    DP_toe_start = DP_toe - np.argmax(np.flip(np.abs(profile[:DP_toe, 0] - profile[DP_toe, 0]) >= delta_x_notch)) + 1
    DP_toe_end = DP_toe + np.argmax(np.abs(profile[DP_toe:, 0] - profile[DP_toe, 0]) >= delta_x_notch) + 1

    # Korrektur der Neigung
    m = 0  # Annahme: keine Regression durchgeführt, m = 0
    av = np.array([1, m])  # Richtungsvektor
    av_ortho = np.array([-av[1], av[0]])  # Orthogonaler Vektor
    av_ortho_norm = av_ortho / np.linalg.norm(av_ortho)

    # Berechne lokale y-Werte
    local_y = profile[:, 0] * np.sin(np.arctan(m)) + profile[:, 1] * np.cos(np.arctan(m))

    # Vorberechnung der Distanzen zwischen Profilpunkten und Mittelpunkt
    distances = np.sqrt((profile[:, 0][:, None] - profile[:, 0])**2 + (profile[:, 1][:, None] - profile[:, 1])**2)

    bestQ = 1000  # Initialer hoher Wert für den Quotienten

    for DP_SP in range(DP_toe_start, DP_toe_end + 1):
        SP_x, SP_y = profile[DP_SP, :]

        for rad in np.arange(radius_min, radius_max + radius_delta, radius_delta):
            # Mittelpunkt des Kreises berechnen
            MP_x = SP_x + av_ortho_norm[0] * rad
            MP_y = SP_y + av_ortho_norm[1] * rad

            # Endpunkt (EP) bestimmen
            MPp_x = profile[DP_SP + 1:, 0]
            MPp_y = profile[DP_SP + 1:, 1]
            distances = (MPp_x - MP_x) ** 2 + (MPp_y - MP_y) ** 2
            DP_EP_candidates = np.where(distances <= rad**2 + 0.01)[0]

            if len(DP_EP_candidates) == 0:
                continue

            DP_EP = DP_SP + DP_EP_candidates[-1]

            if local_y[DP_EP] >= local_y[DP_SP] + min(0.1, settings['crit1'] * rad):
                # Maximale Abweichung zwischen Profil und Kreis
                delta_ri = np.abs(np.sqrt((profile[DP_SP + 1:DP_EP, 0] - MP_x)**2 + (profile[DP_SP + 1:DP_EP, 1] - MP_y)**2) - rad)

                # Zählen der Abstände, die größer als das Kriterium sind
                count_larger = np.sum(delta_ri >= settings['crit2'])

                if count_larger == 0:
                    sum_delta = np.sum(delta_ri)
                    n_DP = len(delta_ri)
                    Qk = sum_delta / (n_DP**2)

                    if n_DP >= settings['crit3'] and Qk < bestQ:
                        bestQ = Qk

                        # Ergebnisse speichern
                        results['radius'] = rad
                        results['MP'] = [MP_x, MP_y]
                        results['SP'] = [SP_x, SP_y]
                        results['EP'] = profile[DP_EP, :]
                        results['maxdist'] = np.max(delta_ri)
                        results['DP_SP'] = DP_SP
                        results['DP_EP'] = DP_EP

    return results
