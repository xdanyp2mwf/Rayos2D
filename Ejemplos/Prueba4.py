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


Prisma = Objetos.TrianguloEquilatero((-5,-0), 7, material = Materiales.BK7)
Sol_Colimado = Fuentes.Fuentes.haz_colimado((-12,0), 0.2 , (1, 0.1), 200, lam_dist="gaussiana",lam = 0.550,lam_ancho=0.2)

Sistema = Evolucion.SistemaOptico(Prisma,Sol_Colimado)

Sistema.evolucionar(pasos = 3000)
Sistema.graficar()
plt.title("Luz del sol colimada pasando por un prisma equilatero", color='white', fontsize=16, pad=20)
 

plt.show()