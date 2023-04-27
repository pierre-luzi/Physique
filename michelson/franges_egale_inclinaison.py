# -*-coding:utf-8 -*

"""Ce programme permet d'afficher la figure d'interférence produite par un Michelson
réglé en lame d'air.
Il est possible de faire varier l'épaisseur de la lame d'air et la longueur d'onde de
la source lumineuse.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, RadioButtons, CheckButtons

def intensity(x, y, wavelength, epaisseur):
    """Calcule l'intensité lumineuse.
    Arguments :
        - x : abscisse sur l'écran ;
        - y : ordonnée sur l'écran ;
        - wavelength : longueur d'onde de la source lumineuse ;
        - epaisseur : épaisseur de la lame d'air.
    """
    return 1 + np.cos(2 * np.pi / wavelength * 2 * epaisseur * (1 - (x**2 + y**2)/(2 * 10**2)))

def update_graphe(val):
    """Fonction de mise à jour du graphe"""
    # Mise à jour des paramètres
    wavelength = slider_wavelength.val
    epaisseur = slider_epaisseur.val

    # Mise à jour du graphe
    graphe = ax.imshow(intensity(x, y, wavelength, epaisseur), interpolation="bicubic", origin="lower", extent=[-1, 1, -1, 1])
    fig.canvas.draw_idle()

# Initialisation des paramètres
wavelength = 500.e-9    # longueur d'onde
epaisseur = 1.e-5       # épaisseur de la lame d'air

# Création de la grille
x = np.linspace(-0.5, 0.5, 50)
y = np.linspace(-0.5, 0.5, 50)
x, y = np.meshgrid(x, y)

fig, ax = plt.subplots()
plt.subplots_adjust(bottom=0.23)

graphe = ax.imshow(intensity(x, y, wavelength, epaisseur), interpolation="bicubic", origin="lower", extent=[-1, 1, -1, 1])
fig.colorbar(graphe)

# Création du slider pour modifier la résistance
ax_wavelength = plt.axes([0.1, 0.07, 0.65, 0.03])
slider_wavelength = Slider(ax_wavelength, r'#lambda', 400.e-9, 750.e-9, valinit=500.e-9)

# Création du slider pour modifier la capacité
ax_epaisseur = plt.axes([0.1, 0.04, 0.65, 0.03])
slider_epaisseur = Slider(ax_epaisseur, r'e', 1.e-5, 5.e-4, valinit=1.e-5)

# Mise à jour du graphe lors d'un changement de paramètre
slider_wavelength.on_changed(update_graphe)
slider_epaisseur.on_changed(update_graphe)

plt.show()