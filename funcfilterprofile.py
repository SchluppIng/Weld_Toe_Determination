import numpy as np
import pandas as pd
from scipy.signal import medfilt
from scipy.interpolate import UnivariateSpline

def funcfilterprofile(profile, settings):
    if settings['filter'] == 'Smoothing Spline':
        profile_filtered = profile.copy()
        spline = UnivariateSpline(profile[:, 0], profile[:, 1], s=settings['smoothparam'])
        profile_filtered[:, 1] = spline(profile_filtered[:, 0])
    elif settings['filter'] == 'Moving Average':
        profile_filtered = profile.copy()
        profile_filtered[:, 1] = pd.Series(profile[:, 1]).rolling(window=int(settings['smoothparam']), min_periods=1, center=True).mean().to_numpy()
    elif settings['filter'] == 'Median':
        profile_filtered = profile.copy()
        profile_filtered[:, 1] = medfilt(profile[:, 1], kernel_size=int(settings['smoothparam']))
    elif settings['filter'] == 'Moving Average + Median':
        profile_filtered = profile.copy()
        if len(settings['smoothparam']) != 2:
            raise ValueError('A vector as Smoothparameter is required for this filter method')
        profile_filtered[:, 1] = pd.Series(profile[:, 1]).rolling(window=int(settings['smoothparam'][0]), min_periods=1, center=True).mean().to_numpy()
        profile_filtered[:, 1] = medfilt(profile_filtered[:, 1], kernel_size=int(settings['smoothparam'][1]))
    elif settings['filter'] == 'Median + Moving Average':
        profile_filtered = profile.copy()
        if len(settings['smoothparam']) != 2:
            raise ValueError('A vector as Smoothparameter is required for this filter method')
        profile_filtered[:, 1] = medfilt(profile[:, 1], kernel_size=int(settings['smoothparam'][0]))
        profile_filtered[:, 1] = pd.Series(profile_filtered[:, 1]).rolling(window=int(settings['smoothparam'][1]), min_periods=1, center=True).mean().to_numpy()
    elif settings['filter'] == 'none':
        profile_filtered = profile
    else:
        raise ValueError('Unknown filtermethod')

    return profile_filtered