
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
Sol =  Fuentes.Fuentes.haz_colimado((-8,12),29,(1,-1),700, lam=0.60)
Agua = Objetos.Interfaz((-0,-2),(0,1), material=Materiales.Agua,longitud=30)


Sistema = Evolucion.SistemaOptico(Agua,Sol)

Sistema.evolucionar(pasos = 4000)
Sistema.graficar()
plt.title("Refracción de la luz del sol en el agua", color='white', fontsize=16, pad=20)
plt.axhspan(-11, -2, color='deepskyblue', alpha=0.4, zorder=1)
plt.axis('equal')
plt.xlim(-10, 10)
plt.ylim(-10, 10)


plt.show()