import numpy as np
from scipy.interpolate import UnivariateSpline

def func_derivation(profile, smoothparam):
    """
    Berechnet den Gradienten und die Krümmung eines Profils.

    Parameters:
        profile (numpy.ndarray): Ein 2D-Array mit x- und y-Werten.
        smoothparam (float): Glättungsparameter, muss zwischen 0.8 und 1.0 liegen.

    Returns:
        gradient (numpy.ndarray): Gradient des Profils.
        curvature (numpy.ndarray): Krümmung des Profils.
    """
    if 0.8 <= smoothparam < 1.0:
        # Glättung des Profils mit einem Smoothing-Spline
        spline_x = UnivariateSpline(profile[:, 0], profile[:, 1], s=smoothparam)
        smoothed_y = spline_x(profile[:, 0])
        profile = np.column_stack((profile[:, 0], smoothed_y))
    elif smoothparam == 1.0:
        pass
    else:
        raise ValueError("smoothparam must be between 0.8 and 1.0!")

    # Erste Ableitung
    diff1_x = profile[:-1, 0] + np.diff(profile[:, 0]) / 2
    diff1_y = np.diff(profile[:, 1]) / np.diff(profile[:, 0])
    diff1 = np.column_stack((diff1_x, diff1_y))

    # Zweite Ableitung
    diff2_x = diff1[:-1, 0] + np.diff(diff1[:, 0]) / 2
    diff2_y = np.diff(diff1[:, 1]) / np.diff(diff1[:, 0])
    diff2 = np.column_stack((diff2_x, diff2_y))

    # Gradient (erste Ableitung mit Länge wie zweite Ableitung)
    gradient_x = diff1[:-1, 0] + np.diff(diff1[:, 0]) / 2
    gradient_y = diff1[:-1, 1] + np.diff(diff1[:, 1]) / 2
    gradient = np.column_stack((gradient_x, gradient_y))

    # Krümmung
    curvature_x = gradient[:, 0]
    curvature_y = diff2[:, 1] / ((1 + gradient[:, 1]**2)**(3 / 2))
    curvature = np.column_stack((curvature_x, curvature_y))

    return gradient, curvature
