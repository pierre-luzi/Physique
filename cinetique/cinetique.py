# -*-coding:utf-8 -*

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, RadioButtons, CheckButtons

def calcul_concentration(concentration_initiale, temps, cste_vitesse, ordre):
    """Calcul de la concentration en fonction du temps"""
    if ordre == 0:
        return concentration_initiale - cste_vitesse * temps
    elif ordre == 1:
        return concentration_initiale * np.exp(-cste_vitesse * temps)
    elif ordre == 2:
        return concentration_initiale / (1 + cste_vitesse * concentration_initiale * temps)
    return None

def activated_radio_button(x, list):
    """Fonction pour récupérer la valeur d'un bouton radio"""
    for i in range(len(x.circles)):
        if x.circles[i].get_facecolor()[0] < 0.5:
            return list[i]

def update_graphe(val):
    concentration_initiale = slider_concentration_initiale.val
    cste_vitesse = slider_cste_vitesse.val
    ordre = activated_radio_button(radio_ordre, ordres)
    concentration = calcul_concentration(concentration_initiale, temps, cste_vitesse, ordre)
    graphe.set_ydata(concentration)
    fig.canvas.draw_idle()
  
# Création de la figure
fig = plt.figure()
plt.subplots_adjust(bottom=0.23)
# plt.rcParams['text.usetex'] = True  # activation de LaTeX

# Initialisation des paramètres
concentration_initiale = 1.
cste_vitesse = 0.05
ordres = [0, 1, 2]
ordre = ordres[1]

temps = np.linspace(0, 100, num=100)
concentration = calcul_concentration(concentration_initiale, temps, cste_vitesse, ordre)

# Création du graphe de la concentration en fonction du temps.
graphe, = plt.plot(temps, concentration, 'r-', lw=2)
plt.axis([0., 100, 0, 1.1*concentration_initiale])
plt.xlabel("Temps (s)")
plt.ylabel("Concentration du réactif (mol/L)")
plt.title("Concentration d'un réactif en fonction du temps")

# Création du slider pour modifier la concentration initiale
ax_concentration_initiale = plt.axes([0.2, 0.1, 0.65, 0.03])
slider_concentration_initiale = Slider(ax_concentration_initiale, r'C_0', 0.2, 1., valinit=1.)

# Créaction du slider pour modifier la constante de vitesse
ax_cste_vitesse = plt.axes([0.2, 0.07, 0.65, 0.03])
slider_cste_vitesse = Slider(ax_cste_vitesse, r'k', 0.01, 0.1, valinit=0.05)

# Création des boutons radio pour choisir l'ordre de la réaction
ax_ordre = plt.axes([0.65, 0.65, 0.22, 0.15], title='Ordre de la réaction')
radio_ordre = RadioButtons(ax_ordre, ordres, active=1)

# Mise à jour lors d'un changement de valeur
slider_concentration_initiale.on_changed(update_graphe)
slider_cste_vitesse.on_changed(update_graphe)
radio_ordre.on_clicked(update_graphe)

plt.show()