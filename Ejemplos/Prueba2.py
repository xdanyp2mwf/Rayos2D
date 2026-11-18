# --- No es necesario instalar el paquete ------------------------
import sys
import os
import matplotlib.pyplot as plt
import numpy as np


sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from rayos2d import * 
# -------------------------------------------------------------

"""
# ---------------Si ya está instalado --------------------------

from rayos2d import * 
import matplotlib.pyplot as plt
import numpy as np
#---------------------------------------------------------------
"""

Foco =  Fuentes.Fuentes.fuente_puntual((3,3),700)
Agua = Objetos.Interfaz((-2.5,-2),(0,1), material=Materiales.Agua)

Sistema = Evolucion.SistemaOptico(Agua,Foco)

Sistema.evolucionar(pasos = 4000)
Sistema.graficar()
plt.title("Refracción de la luz de un foco en el agua", color='white', fontsize=16, pad=20)
plt.axhspan(-15, -2, color='deepskyblue', alpha=0.4, zorder=1)


plt.show()