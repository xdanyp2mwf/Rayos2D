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

LenteBiconcava = Objetos.Lente(-3, -0,  -6, 6, 3, 8, material = Materiales.SF10,num_puntos=2000)
Sol =  Fuentes.Fuentes.haz_colimado((-12,0),8,(1,-0.05),700, lam=0.60)

Sistema = Evolucion.SistemaOptico(LenteBiconcava,Sol)

Sistema.evolucionar(pasos = 3000)
Sistema.graficar()
plt.title("Luz de una linterna pasando por lente biconcava ", color='white', fontsize=16, pad=20)


plt.show()