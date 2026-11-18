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


LenteCircular = Objetos.Lente(-0, -0, 4, -4, 8, 8, material = Materiales.BK7)
Foco =  Fuentes.Fuentes.fuente_puntual((-2,0),700,lam=0.65, lam_dist= "uniforme", lam_ancho=0.00,angulo_apertura=360)


Sistema = Evolucion.SistemaOptico(LenteCircular,Foco)

Sistema.evolucionar(pasos = 4000)
Sistema.graficar()
plt.title("Luz de un foco saliendo de una lente circular", color='white', fontsize=16, pad=20)


plt.show()