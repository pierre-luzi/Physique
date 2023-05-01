# -*-coding:utf-8 -*

"""
Ce programme permet d'illustrer le phénomène de battements.
Deux signaux sinusoïdaux de fréquences proches sont sommés.
La fréquence des signaux peut être modifiée grâce à des sliders.
"""

import cmath, math
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.widgets import Slider, Button, RadioButtons, CheckButtons


N_SAMPLES = 1000


def update_graphe(val):
    """Fonction de mise à jour du graphe"""
    # Mise à jour des paramètres à partir des sliders
    frequence1 = s_frequence1.val
    frequence2 = s_frequence2.val
    
    # Calcul des signaux
    sig1 = np.sin(2 * np.pi * frequence1 * temps)
    sig2 = np.sin(2 * np.pi * frequence2 * temps)
    signal = sig1 + sig2
    enveloppe = 2 * np.cos(np.pi * (frequence1 - frequence2) * temps)
    
    # Mise à jour des graphes
    graphe1.set_ydata(sig1)
    graphe2.set_ydata(sig2)
    graphe_somme.set_ydata(signal)
    graphe_enveloppe1.set_ydata(enveloppe)
    graphe_enveloppe2.set_ydata(-enveloppe)
    fig.canvas.draw_idle()


# Initialisation des fréquences
frequence1 = 440.
frequence2 = 440.

# Création de la figure
fig, ax = plt.subplots(3, sharex=True)
plt.subplots_adjust(bottom=0.25)

# Création des signaux
temps = np.linspace(0, 50e-3, N_SAMPLES)
sig1 = np.sin(2 * np.pi * frequence1 * temps)
sig2 = np.sin(2 * np.pi * frequence2 * temps)
signal = sig1 + sig2
enveloppe = 2 * np.cos(np.pi * (frequence1 - frequence2) * temps)

# Tracé des graphes
graphe1, = ax[0].plot(temps, sig1, lw=2, color='red')
graphe2, = ax[1].plot(temps, sig2, lw=2, color='red')
graphe_somme, = ax[2].plot(temps, signal, lw=2, color='red')
graphe_enveloppe1, = ax[2].plot(temps, enveloppe, lw=2, color='b', linestyle='--')
graphe_enveloppe2, = ax[2].plot(temps, -enveloppe, lw=2, color='b', linestyle='--')

# Paramètres des axes
ax[0].axis([temps[0], temps[-1], -1.1, 1.1]) # Limites des axes (xmin,xmax,ymin,ymax)
ax[1].axis([temps[0], temps[-1], -1.1, 1.1]) # Limites des axes (xmin,xmax,ymin,ymax)
ax[2].axis([temps[0], temps[-1], -2.2, 2.2]) # Limites des axes (xmin,xmax,ymin,ymax)

ax[0].set_ylabel('Amplitude')
ax[1].set_ylabel('Amplitude')
ax[2].set_ylabel('Amplitude')
ax[2].set_xlabel('Temps (s)')

# Création du slider pour modifier la fréquence du signal 1
ax_frequence1 = plt.axes([0.1, 0.1, 0.8, 0.03])
s_frequence1 = Slider(ax_frequence1, 'f_1', 240, 640, valinit=frequence1)

# Création du slider pour modifier la fréquence du signal 2
ax_frequence2 = plt.axes([0.1, 0.07, 0.8, 0.03])
s_frequence2 = Slider(ax_frequence2, 'f_2', 240, 640, valinit=frequence2)

s_frequence1.on_changed(update_graphe)
s_frequence2.on_changed(update_graphe)

   



# # Creation du bouton de "reset"
# resetax = plt.axes([0.8, 0.015, 0.1, 0.04])
# button = Button(resetax, 'Reset', color=axcolor, hovercolor='0.975')
# # Definition de la fonction de "reset" (valeurs par defaut)
# def reset(event):
#     s_N.reset() # La methode .reset() appliquee a la barre s_N lui redonne sa valeur valinit, soit f0
#     s_a.reset() # La methode .reset() appliquee a la barre s_a lui redonne sa valeur valinit, soit a0
#     s_b.reset() # La methode .reset() appliquee a la barre s_b lui redonne sa valeur valinit, soit t0
#     s_lamb.reset() # La methode .reset() appliquee a la barre s_lamb lui redonne sa valeur valinit, soit t0
#
# button.on_clicked(reset) # Lorsqu'on clique sur "reset", on applique la fonction reset definie au dessus
#
# # Creation du menu de selection des traces a afficher
# cax = plt.axes([0.015, 0.3, 0.2, 0.15], axisbg=axcolor)
# check = CheckButtons(cax, ('Fonction', 'Facteur de forme', 'Facteur de structure'), (True, False, False))
# # Definition de la fonction qui passe un affichage de visible a invisible
# def chooseplot(label):
#     if label == 'Fonction': l.set_visible(not l.get_visible()) # Si on clique sur le bouton "Fonction", la trace 'l' passe visible si elle ne l'etait pas, et vice versa
#     elif label == 'Facteur de forme': l_forme.set_visible(not l_forme.get_visible()) # Si on clique sur le bouton "Facteur de forme", la trace 'l_forme' passe visible si elle ne l'etait pas, et vice versa
#     elif label == 'Facteur de structure': l_structure.set_visible(not l_structure.get_visible()) # Si on clique sur le bouton "Facteur de structure", la trace 'l_structure' passe visible si elle ne l'etait pas, et vice versa
#     fig.canvas.draw_idle() # On provoque la mise a jour du graphique, qui n'est pas automatique par defaut
# check.on_clicked(chooseplot) # Lorsqu'on coche un de ces boutons, on applique la fonction chooseplot

plt.show() # On provoque l'affichage a l'ecran
