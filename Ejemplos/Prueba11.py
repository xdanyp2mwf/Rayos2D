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


Corazon = Objetos.Corazon((0,0),escala=5, material=Materiales.Diamante )
Sol =  Fuentes.Fuentes.haz_colimado((0,-11),22,(0.0,1),2000, lam=0.65)


Sistema = Evolucion.SistemaOptico(Corazon,Sol)

Sistema.evolucionar(pasos = 6000)
Sistema.graficar()
plt.title("Te amo, hoy y siempre", 
          color='white', 
          fontsize=22, 
          pad=20, 
          fontname='serif',      
          fontweight='bold',     
          fontstyle='italic')


plt.show()