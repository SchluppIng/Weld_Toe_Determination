import matplotlib.pyplot as plt
import numpy as np

def funcfigresult(profile, radiusresults, angleresults):
    """
    Erstellt ein Diagramm, das Kreise und Linien aus den Ergebnissen sowie das Profil darstellt.

    Parameters:
    profile (np.ndarray): 2D-Array mit den Profilpunkten (x, y).
    radiusresults (list of dict): Liste mit Radius-Ergebnissen, jedes als Dictionary mit Schlüsseln:
                                   - 'MP': Mittelpunkt des Kreises [x, y].
                                   - 'radius': Radius des Kreises.
                                   - 'method': Methode der Radiusberechnung.
    angleresults (list of dict): Liste mit Winkel-Ergebnissen, jedes als Dictionary mit Schlüsseln:
                                   - 'angle': Winkel in Grad.
                                   - 'DP': Index des Datenpunkts für den Winkel.
                                   - 'sign': Vorzeichen des Winkels.
    """
    # Einstellungen
    colors = ['b', 'r', 'g']
    circlestyles = ['-', '--', '--']
    linestyles = ['-', '--', '--']

    # Figur und Achse erstellen
    fig, ax = plt.subplots(figsize=(8 / 2.54, 6 / 2.54))  # Umrechnung von cm in inch

    # Kreise plotten
    legend_entries = []
    if radiusresults:
        for circle_nr, radiusresult in enumerate(radiusresults):
            theta = np.linspace(0, 2 * np.pi, 100)
            x_circle = radiusresult['MP'][0] + radiusresult['radius'] * np.cos(theta)
            y_circle = radiusresult['MP'][1] + radiusresult['radius'] * np.sin(theta)
            ax.plot(x_circle, y_circle, color=colors[circle_nr], linestyle=circlestyles[circle_nr], linewidth=1)
            legend_entries.append(radiusresult['method'])

    # Linien für den Schweißnahtwinkel plotten
    if angleresults:
        for line_nr, angleresult in enumerate(angleresults):
            m = angleresult['sign'] * np.tan(np.radians(angleresult['angle']))
            b = profile[angleresult['DP'], 1] - m * profile[angleresult['DP'], 0]

            y_line = [np.min(profile[:, 1]) - 1, np.max(profile[:, 1])]
            x_line = [(y - b) / m for y in y_line]
            ax.plot(x_line, y_line, color=colors[line_nr], linestyle=linestyles[line_nr], linewidth=1)

    # Profil plotten
    ax.plot(profile[:, 0], profile[:, 1], '-', color='k', linewidth=1.0)

    # Achseneigenschaften
    ax.set_xlabel('x [mm]', fontname='Arial', fontsize=9)
    ax.set_ylabel('y [mm]', fontname='Arial', fontsize=9)
    ax.tick_params(axis='both', labelsize=9)
    ax.grid(False)
    ax.set_aspect('auto', adjustable='datalim')

    # X- und Y-Achsenbegrenzungen setzen
    if radiusresults:
        center_x = radiusresults[0]['MP'][0]
        center_y = radiusresults[0]['MP'][1]
        radius = radiusresults[0]['radius']
        ax.set_xlim([center_x - radius * 2, center_x + radius * 2])
        min_y = center_y - radius * 1.5
        max_y = min_y + (ax.get_position().height / ax.get_position().width) * (ax.get_xlim()[1] - ax.get_xlim()[0])
        ax.set_ylim([min_y, max_y])

    # Legende hinzufügen
    if legend_entries:
        ax.legend(legend_entries, loc='best', fontsize=8)

    # Diagramm anzeigen
    plt.tight_layout()
    plt.show()
