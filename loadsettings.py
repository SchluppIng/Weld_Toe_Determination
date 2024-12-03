def loadsettings():
    """
    Load settings for data processing and evaluation.
    Returns:
        dict: Dictionary containing all settings.
    """
    settings = {
        # Plot settings
        'plotresult': 'on',  # 'on' to enable plotting, 'off' to disable

        # Data processing
        'outliermethod': 'none',  # 'remove' or 'none'
        'filter': 'none',  # 'Smoothing Spline', 'Moving Average and Median', or 'none'
        'smoothparam': 0.995,  # For 'Smoothing Spline' filter method
        'ordermethod': 'none',  # 'ordered' or 'none'
        'orderdistance': 0.05,  # New x distance between points (in mm)
        'interpmethod': 'linear',  # Interpolation method

        # Data evaluation
        'CM': {
            'smoothparam': 1  # Curvature method smooth parameter
        },
        'LSM': {
            'smoothparam': 1,  # Least Squares Method smooth parameter
            'factor': 0.3  # Factor for LSM
        },
        'IM': {
            'smoothparam': 1,  # Iteration Method smooth parameter
            'crit1': 0.01,  # End point criterion (factor of weld toe radius)
            'crit2': 0.02,  # Max distance between profile and circle
            'crit3': 3  # Data points between starting and end point
        },
        'Angle': {
            'smoothparam': 1,  # Angle methods smooth parameter
            'smoothlen': 0.2  # Smooth length for angle methods
        }
    }

    return settings
