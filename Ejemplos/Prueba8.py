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

ParedSup = Objetos.Interfaz((0, 2.5), (0, -1), material=Materiales.Aire, longitud=30)
ParedInf = Objetos.Interfaz((0, -2.5), (0, 1), material=Materiales.Aire, longitud=30)
FocoInterno = Fuentes.Fuentes.fuente_puntual((-18, 0), 150, lam=0.52,angulo_apertura=70)

Sistema = Evolucion.SistemaOptico([ParedSup, ParedInf], FocoInterno, ambiente=Materiales.BK7)

Sistema.evolucionar(pasos=5000)
Sistema.graficar()
plt.title("Propagación por reflexión total interna en guía de ondas", color='white', fontsize=16, pad=20)
plt.axhspan(-2.5, 2.5, color='cyan', alpha=0.15, zorder=1)

plt.show()