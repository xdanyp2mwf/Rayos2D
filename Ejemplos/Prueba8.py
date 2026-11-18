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


LenteBiconvexa = Objetos.Lente(-3, -0,  6, -6, 1.5, 5, material = Materiales.SF10,num_puntos=2000)
Sol =  Fuentes.Fuentes.haz_colimado((-12,5),29,(1,-0.3),700, lam=0.60)



Sistema = Evolucion.SistemaOptico(LenteBiconvexa, Sol)

Sistema.evolucionar(pasos = 4000)
Sistema.graficar()
plt.title("Luz del sol pasando por lente biconvexa", color='white', fontsize=16, pad=20)


plt.show()