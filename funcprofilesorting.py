import numpy as np
from scipy.interpolate import interp1d

def funcprofilesorting(profile, settings):
    if settings['ordermethod'] == 'ordered':
        xdelta = settings['orderdistance']
        xmin = np.ceil(np.min(profile[:, 0]))
        xmax = np.floor(np.max(profile[:, 0]))

        # Entfernen von Duplikaten basierend auf der ersten Spalte
        _, unique_indices = np.unique(profile[:, 0], return_index=True)
        profile = profile[unique_indices]

        xq = np.arange(xmin, xmax + xdelta, xdelta)  # Neue x-Werte mit dem gegebenen Abstand
        interpolator = interp1d(profile[:, 0], profile[:, 1], kind=settings['interpmethod'], fill_value='extrapolate')
        vq = interpolator(xq)

        profile_new = np.column_stack((xq, vq))
    elif settings['ordermethod'] == 'none':
        profile_new = profile
    else:
        raise ValueError('Unknown ordermethod')

    return profile_new