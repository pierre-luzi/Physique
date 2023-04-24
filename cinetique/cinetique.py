# -*-coding:utf-8 -*

"""Ce programme permet d'afficher l'évolution de la concentration d'un réactif au cours du temps.
Il est possible de modifier plusieurs paramètres de manière interactive :
    - la concentration initiale C_0 ;
    - la constante de vitesse k ;
    - l'ordre de la réaction.

On considère uniquement une loi de vitesse dont l'ordre global est aussi l'ordre partiel du réactif :
    dC/dt = - k C^ordre
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, RadioButtons, CheckButtons

def calcul_concentration(concentration_initiale, temps, cste_vitesse, ordre):
    """Calcul de la concentration au cours du temps"""
    if ordre == 0:
        return concentration_initiale - cste_vitesse * temps
    elif ordre == 1:
        return concentration_initiale * np.exp(-cste_vitesse * temps)
    elif ordre == 2:
        return concentration_initiale / (1 + cste_vitesse * concentration_initiale * temps)
    return None

def calcul_temps_demi_reaction(concentration_initiale, cste_vitesse, ordre):
    """Calcul du temps de demi-réaction"""
    if ordre == 0:
        return concentration_initiale / (2 * cste_vitesse)
    elif ordre == 1:
        return np.log(2) / cste_vitesse
    elif ordre == 2:
        return 1. / (cste_vitesse * concentration_initiale)

def activated_radio_button(x, list):
    """Fonction pour récupérer la valeur d'un bouton radio"""
    for i in range(len(x.circles)):
        if x.circles[i].get_facecolor()[0] < 0.5:
            return list[i]

def update_graphe(val):
    """Fonction de mise à jour du graphe"""
    # Mise à jour des paramètres
    concentration_initiale = slider_concentration_initiale.val
    cste_vitesse = slider_cste_vitesse.val
    ordre = activated_radio_button(radio_ordre, ordres)
    
    # Calcul de la concentration au cours du temps et du temps de demi-réaction
    concentration = calcul_concentration(concentration_initiale, temps, cste_vitesse, ordre)
    temps_demi_reaction = calcul_temps_demi_reaction(concentration_initiale, cste_vitesse, ordre)
    
    # Mise à jour du graphe
    graphe.set_ydata(concentration)
    x_temps_demi_reaction.set_xdata([temps_demi_reaction, temps_demi_reaction])
    x_temps_demi_reaction.set_ydata([0., 0.5*concentration_initiale])
    y_temps_demi_reaction.set_xdata([0., temps_demi_reaction])
    y_temps_demi_reaction.set_ydata([0.5*concentration_initiale, 0.5*concentration_initiale])
    fig.canvas.draw_idle()
  
# Création de la figure
fig = plt.figure()
plt.subplots_adjust(bottom=0.23)

# Initialisation des paramètres
concentration_initiale = 1      # initialisation de la concentration initiale
cste_vitesse = 0.05             # initialisation de la constante de vitesse
ordres = [0, 1, 2]              # ordres pris en compte pour le calcul de la concentration
ordre = ordres[1]               # initialisation de l'ordre

# Calcul de la concentration au cours du temps et du temps de demi-réaction
temps = np.linspace(0, 100, num=100)
concentration = calcul_concentration(concentration_initiale, temps, cste_vitesse, ordre)
temps_demi_reaction = calcul_temps_demi_reaction(concentration_initiale, cste_vitesse, ordre)

# Création du graphe de la concentration en fonction du temps.
plt.axis([0., 100, 0, 1.1*concentration_initiale])
plt.xlabel("Temps (s)")
plt.ylabel("Concentration du réactif (mol/L)")
plt.title("Concentration d'un réactif en fonction du temps")
graphe, = plt.plot(temps, concentration, 'r-', lw=2)

# Tracé des droites permettant de lire le temps de demi-réaction
x_temps_demi_reaction, = plt.plot([temps_demi_reaction, temps_demi_reaction], [0., 0.5*concentration_initiale], c='g', ls='--')
y_temps_demi_reaction, = plt.plot([0., temps_demi_reaction], [0.5*concentration_initiale, 0.5*concentration_initiale], c='g', ls='--')

# Création du slider pour modifier la concentration initiale
ax_concentration_initiale = plt.axes([0.1, 0.1, 0.65, 0.03])
slider_concentration_initiale = Slider(ax_concentration_initiale, r'C_0', 0.2, 1., valinit=1.)

# Créaction du slider pour modifier la constante de vitesse
ax_cste_vitesse = plt.axes([0.1, 0.04, 0.65, 0.03])
slider_cste_vitesse = Slider(ax_cste_vitesse, r'k', 0.01, 0.1, valinit=0.05)

# Création des boutons radio pour choisir l'ordre de la réaction
ax_ordre = plt.axes([0.65, 0.65, 0.22, 0.15], title='Ordre de la réaction')
radio_ordre = RadioButtons(ax_ordre, ordres, active=1)

# Mise à jour lors d'un changement de valeur
slider_concentration_initiale.on_changed(update_graphe)
slider_cste_vitesse.on_changed(update_graphe)
radio_ordre.on_clicked(update_graphe)

plt.show()