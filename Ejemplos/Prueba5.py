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

Objetivo = Objetos.Lente((-8, 0), (10, -10), 1.9, 8, material=Materiales.BK7)
Ocular = Objetos.Lente((4.9, 0), (3, -3), 1.6, 4, material=Materiales.BK7)
Estrella = Fuentes.Fuentes.haz_colimado((-14, 0), 5, (1, 0), 100, lam=0.53)

Sistema = Evolucion.SistemaOptico([Objetivo, Ocular], Estrella)

Sistema.evolucionar(pasos=4000)
Sistema.graficar()
plt.title("Telescopio refractor simple (dos lentes convergentes)", color='white', fontsize=16, pad=20)

plt.show()