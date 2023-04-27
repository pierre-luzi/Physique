# -*-coding:utf-8 -*

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, RadioButtons, CheckButtons

N_SAMPLES = 1000

def transfer_function(omega, tau):
    return 1./(1 + 1j * omega * tau)

def update_graphe(val):
    """Fonction de mise à jour du graphe"""
    # Mise à jour des paramètres
    resistance = pow(10, slider_resistance.val)
    slider_resistance.valtext.set_text("{:.2E}".format(resistance))
    capacity = pow(10, slider_capacity.val)
    slider_capacity.valtext.set_text("{:.2E}".format(capacity))
    
    # Calcul de la fonction de transfert
    h = transfer_function(2*np.pi*x, resistance * capacity)
    
    # Mise à jour du graphe
    amplitude.set_ydata(np.abs(h))
    phase.set_ydata(180/np.pi * np.angle(h))
    fig.canvas.draw_idle()

# Initialisation des valeurs des composants
resistance = 100
capacity = 1.e-7

x = np.logspace(1, 8, N_SAMPLES)
h = transfer_function(2*np.pi*x, resistance * capacity)

fig, (ax1, ax2) = plt.subplots(nrows=2, sharex=True)
plt.subplots_adjust(bottom=0.23)

amplitude, = ax1.loglog(x, np.abs(h), 'r-')
ax1.set_xlim([1.e1, 1.e8])
ax1.set_ylim([0.1, 1.1])
ax1.set_ylabel('Amplitude')

phase, = ax2.semilogx(x, 180/np.pi * np.angle(h), 'r-')
ax2.set_ylim([-90, 0])
ax2.set_xlabel('Fréquence (Hz)')
ax2.set_ylabel('Phase (°)')

fig.suptitle('Diagramme de Bode d\'un filtre RC')

# Création du slider pour modifier la résistance
ax_resistance = plt.axes([0.1, 0.07, 0.65, 0.03])
slider_resistance = Slider(ax_resistance, r'R', 1, 5, valinit=np.log10(resistance))
slider_resistance.valtext.set_text("{:.2E}".format(resistance))

# Création du slider pour modifier la capacité
ax_capacity = plt.axes([0.1, 0.04, 0.65, 0.03])
slider_capacity = Slider(ax_capacity, r'C', -9, -6, valinit=np.log10(capacity))
slider_capacity.valtext.set_text("{:.2E}".format(capacity))

slider_resistance.on_changed(update_graphe)
slider_capacity.on_changed(update_graphe)

plt.show()