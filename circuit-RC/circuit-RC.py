# -*-coding:utf-8 -*

"""
Ce programme représente le diagramme de Bode (amplitude, phase)
d'un filtre passe-bas réalisé grâce à un circuit RC.
Il représente également un signal d'excitation et le signal de sortie.
On peut régler les valeurs de la résistance et de la capacité.
"""

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
    tau = resistance * capacity
    h = transfer_function(2*np.pi*frequency, tau)
    
    # Callcul de l'amplitude et de la phase du signal de sortie
    exit_bode = transfer_function(2*np.pi * excitation_frequency, resistance * capacity)
    exit_amplitude = np.abs(exit_bode)
    exit_phase = np.angle(exit_bode)
    
    # Mise à jour du graphe
    amplitude.set_ydata(np.abs(h))
    phase.set_ydata(180/np.pi * np.angle(h))
    exit.set_ydata(exit_amplitude * np.sin(2*np.pi * excitation_frequency * time + exit_phase))
    x_freq_amplitude.set_ydata([ax['amplitude'].get_ylim()[0], exit_amplitude])
    y_freq_amplitude.set_ydata([exit_amplitude, exit_amplitude])
    x_freq_phase.set_ydata([ax['phase'].get_ylim()[0], 180/np.pi * exit_phase])
    y_freq_phase.set_ydata([180/np.pi * exit_phase, 180/np.pi * exit_phase])
    fig.canvas.draw_idle()


# Initialisation des valeurs des composants
resistance = 100
capacity = 1.e-7


# Création des graphes
mosaic = [
    ['amplitude', '.'],
    ['amplitude', 'signal'],
    ['phase', 'signal'],
    ['phase', '.']
]
fig, ax = plt.subplot_mosaic(mosaic)
plt.tight_layout()
plt.subplots_adjust(bottom=0.23)


# Diagramme de Bode
frequency = np.logspace(1, 8, N_SAMPLES)
tau = resistance * capacity
h = transfer_function(2*np.pi*frequency, tau)

# Diagramme en amplitude
amplitude, = ax['amplitude'].loglog(frequency, np.abs(h), 'r-')
ax['amplitude'].set_xlim(1.e1, 1.e8)
ax['amplitude'].get_xaxis().set_visible(False)
ax['amplitude'].set_ylim([1.e-4, 1.3])
ax['amplitude'].set_ylabel('Amplitude')

# Diagramme de phase
phase, = ax['phase'].semilogx(frequency, 180/np.pi * np.angle(h), 'r-')
ax['phase'].sharex(ax['amplitude'])
ax['phase'].set_ylim([-92, 2])
ax['phase'].set_xlabel('Fréquence (Hz)')
ax['phase'].set_ylabel('Phase (°)')


# Graphe temporel
excitation_frequency = 1.e4
time = np.linspace(0, 5.e-4, N_SAMPLES)

# Signal d'excitation
excitation, = ax['signal'].plot(time, np.sin(2*np.pi * excitation_frequency * time), 'r-')

# Signal de sortie
exit_bode = transfer_function(2*np.pi * excitation_frequency, resistance * capacity)
exit_amplitude = np.abs(exit_bode)
exit_phase = np.angle(exit_bode)
exit, = ax['signal'].plot(time, exit_amplitude * np.sin(2*np.pi * excitation_frequency * time + exit_phase), 'b--')

ax['signal'].set_xlim(0, 5.e-4)
ax['signal'].ticklabel_format(axis='x', style='sci', scilimits=(0,0))   # notation scientifique
ax['signal'].set_ylim(-1.1, 1.1)
ax['signal'].set_xlabel('Temps (s)')
ax['signal'].set_ylabel('Amplitude (V)')

# Tracé des droites permettant de lire le diagramme de Bode
x_freq_amplitude, = ax['amplitude'].plot(
    [excitation_frequency, excitation_frequency],           # abscisse de la droite verticale
    [ax['amplitude'].get_ylim()[0], exit_amplitude],        # ordonnées des extrémités
    c='g', ls='--'
)
y_freq_amplitude, = ax['amplitude'].plot(
    [ax['amplitude'].get_xlim()[0], excitation_frequency],  # abscisses des extrémités
    [exit_amplitude, exit_amplitude],                       # ordonnée de la droite horizontale
    c='g', ls='--'
)
x_freq_phase, = ax['phase'].plot(
    [excitation_frequency, excitation_frequency],           # abscisse de la droite verticale
    [ax['phase'].get_ylim()[0], 180/np.pi * exit_phase],    # ordonnée de la droite horizontale
    c='g', ls='--'
)
y_freq_phase, = ax['phase'].plot(
    [ax['phase'].get_xlim()[0], excitation_frequency],      # abscisses des extrémités
    [180/np.pi * exit_phase, 180/np.pi * exit_phase],       # ordonnée de la droite horizontale
    c='g', ls='--'
)

# fig.suptitle('Diagramme de Bode d\'un filtre RC')


# Création du slider pour modifier la résistance
ax_resistance = plt.axes([0.1, 0.07, 0.65, 0.03])
slider_resistance = Slider(ax_resistance, r'R', 1, 5, valinit=np.log10(resistance))
slider_resistance.valtext.set_text("{:.2E}".format(resistance))     # notation scientifique

# Création du slider pour modifier la capacité
ax_capacity = plt.axes([0.1, 0.04, 0.65, 0.03])
slider_capacity = Slider(ax_capacity, r'C', -9, -6, valinit=np.log10(capacity))
slider_capacity.valtext.set_text("{:.2E}".format(capacity))         # notation scientifique

slider_resistance.on_changed(update_graphe)
slider_capacity.on_changed(update_graphe)

plt.show()