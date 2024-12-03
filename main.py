import os
import numpy as np
import pandas as pd
from loadsettings import loadsettings
from funcremoveoutlier import funcremoveoutlier
from funcfilterprofile import funcfilterprofile
from funcprofilesorting import funcprofilesorting
from funcevalCM import funcevalCM
from funcevalLSM import funcevalLSM
from funcevalIM import funcevalIM
from funcevalangle import funcevalangle
from funcfigresult import funcfigresult


def main():
    # Liste der Dateien für die Auswertung
    folder = os.path.join(r'C:\temp\Python\Weld_Toe_Determination\examples')
    file_list = [f for f in os.listdir(folder) if f.endswith('.asc')]

    # Einstellungen für die Datenverarbeitung laden
    settings = loadsettings()

    # Ergebnisse initialisieren
    allresults = np.full((len(file_list), 6), np.nan)

    for loop_nr, filename in enumerate(file_list):
        # Daten importieren
        filepath = os.path.join(folder, filename)
        data = np.loadtxt(filepath, skiprows=1)  # Annahme: Daten als ASCII-Datei
        profile = data[:, :2]

        # Profil anpassen (cm zu mm und Matrix umdrehen)
        profile *= 10  # Umrechnung von cm zu mm
        profile = np.flipud(profile)  # Matrix umdrehen

        # Datenverarbeitung
        profile = funcremoveoutlier(profile, settings)
        profile = funcfilterprofile(profile, settings)
        profile = funcprofilesorting(profile, settings)

        # Radius-Bewertung
        results_CM = funcevalCM(profile, settings["CM"])
        results_LSM = funcevalLSM(profile, settings["LSM"])
        results_IM = funcevalIM(profile, settings["IM"])

        # Winkel-Bewertung
        angle_MAX = funcevalangle('MAX', profile, settings["Angle"], None)
        angle_END_LSM = funcevalangle('END', profile, settings["Angle"], results_LSM)
        angle_END_IM = funcevalangle('END', profile, settings["Angle"], results_IM)

        # Ergebnisse speichern
        allresults[loop_nr, [0, 1, 2]] = [results_CM["radius"], results_LSM["radius"], results_IM["radius"]]
        allresults[loop_nr, [3, 4, 5]] = [angle_MAX["angle"], angle_END_LSM["angle"], angle_END_IM["angle"]]

         # Ergebnisse im gewünschten Format ausgeben
        print(f"Results for File: {filename}")
        print("-" * 53)
        print(f"Radius (CM method): {results_CM['radius']:.3f} mm")
        print(f"Radius (LSM method): {results_LSM['radius']:.3f} mm")
        print(f"Radius (IM method): {results_IM['radius']:.3f} mm")
        print("-" * 53)
        print(f"Max Angle: {angle_MAX['angle']:.3f} degrees")
        print(f"End Angle (LSM method): {angle_END_LSM['angle']:.3f} degrees")
        print(f"End Angle (IM method): {angle_END_IM['angle']:.3f} degrees")
        print("-" * 53)
        print()  # Leere Zeile für bessere Lesbarkeit

        # Diagramm plotten
        if settings.get("plotresult") == 'on':
            funcfigresult(profile, [results_CM, results_LSM, results_IM],
                          [angle_MAX, angle_END_LSM, angle_END_IM])

if __name__ == "__main__":
    main()