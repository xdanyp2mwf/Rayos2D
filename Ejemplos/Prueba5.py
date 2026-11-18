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

LentePlana = Objetos.Lente(0, 0, -np.inf, np.inf, 2, 10, material = Materiales.CristalComun)
Sol =  Fuentes.Fuentes.haz_colimado((-8,12),29,(1,-1),700, lam=0.60)

Sistema = Evolucion.SistemaOptico(LentePlana,Sol)

Sistema.evolucionar(pasos = 4000)
Sistema.graficar()
plt.title("Luz del sol pasando por lente plana ", color='white', fontsize=16, pad=20)


plt.show()