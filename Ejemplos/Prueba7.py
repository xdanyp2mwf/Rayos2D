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

Prisma1 = Objetos.TrianguloEquilatero((-5, -1), 5, material=Materiales.BK7, direccion=(0, 1))
Prisma2 = Objetos.TrianguloEquilatero((-0.3, -1.2), 5, material=Materiales.BK7, direccion=(0, -1))
LuzBlanca = Fuentes.Fuentes.haz_colimado((-13, -1), 0.2, (1, 0.15), 100, lam_dist="gaussiana", lam=0.55, lam_ancho=0.18)

Sistema = Evolucion.SistemaOptico([Prisma1, Prisma2], LuzBlanca)

Sistema.evolucionar(pasos=4000)
Sistema.graficar()
plt.title("Dispersión y recombinación cromática en doble prisma", color='white', fontsize=16, pad=20)

plt.show()