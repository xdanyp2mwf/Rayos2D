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


LenteCircular = Objetos.Lente(-0, -0, 4, -4, 8, 8, material = Materiales.Diamante)
Laserverde = Fuentes.Fuentes.haz_colimado((-10,0), 0.1 , (1, -0.2), 600,lam = 0.55)



Sistema = Evolucion.SistemaOptico(LenteCircular,Laserverde)

Sistema.evolucionar(pasos = 4000)
Sistema.graficar()
plt.title("Laser verde pasando por una lente circular de diamante", color='white', fontsize=16, pad=20)


plt.show()