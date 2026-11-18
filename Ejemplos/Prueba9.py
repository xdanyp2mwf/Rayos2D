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

EspejoPrimario = Objetos.Lente((9, 0), (-14, np.inf), 1, 12, material=Materiales.Espejo)
EspejoSecundario = Objetos.Interfaz((2.8, 0), (1, -1), material=Materiales.Espejo , longitud=1.5)
Ocular = Objetos.Lente((2.8, -3.7), (2.5, -2.5), 0.6, 2.5, material=Materiales.BK7, direccion=(1, 0))
LuzEstelar = Fuentes.Fuentes.haz_colimado((-14, -0), 5, (1, 0), 200, lam=0.49)

Sistema = Evolucion.SistemaOptico([EspejoPrimario, EspejoSecundario,Ocular], LuzEstelar)

Sistema.evolucionar(pasos=5000)
Sistema.graficar()
plt.title("Telescopio reflector Newtoniano con espejos", color='white', fontsize=16, pad=20)

plt.show()