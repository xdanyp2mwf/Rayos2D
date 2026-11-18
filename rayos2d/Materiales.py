import numpy as np 

class Material:
    def __init__(self, nombre, coeficientes, modelo = 0, es_espejo = False):
        """
        coeficientes: Lista o tupla con [B1, B2, B3, B4, C1, C2, C3, C4]
        modelo == 0 (no es gas)
               == 1 (si es gas)
               => 2 (alguno diferente)
        es_espejo: Booleano. Si es True, el sistema lo tratará como reflectante perfecto.
        """
        self.nombre = nombre
        self.es_espejo = es_espejo 
        
        if coeficientes is None:
            self.B1 = self.B2 = self.B3 = self.B4 = self.C1 = self.C2 = self.C3 = self.C4 = 0
        else:
            self.B1, self.B2, self.B3, self.B4, self.C1, self.C2, self.C3, self.C4 = coeficientes
            
        self.modelo = modelo

    def n(self, lam):
        """
        Calcula el índice de refracción de forma agnóstica (funciona con escalares, numpy y cupy).
        """
        if self.es_espejo:
            # TRUCO: Multiplicar por 0 y sumar 1 mantiene el tipo de dato (GPU o CPU) y la forma del array
            return (lam * 0) + 1.0 

        if self.modelo == 0:
            l2 = lam ** 2 
            
            term1 = (self.B1 * l2) / (l2 - self.C1) 
            term2 = (self.B2 * l2) / (l2 - self.C2)
            term3 = (self.B3 * l2) / (l2 - self.C3)
            term4 = (self.B4 * l2) / (l2 - self.C4)
            
            n2 = 1 + term1 + term2 + term3 + term4
            
            # TRUCO: Usar ** 0.5 en lugar de np.sqrt para compatibilidad universal
            return n2 ** 0.5
        
        elif self.modelo == 1:
            l2 = 1 / (lam**2)
            delta_n = (self.B1/(self.C1-l2)) + (self.B2/(self.C2-l2))
            return 1.0 + delta_n
        
        else:
            return  self.B1 - self.B2*lam**2 + self.B3*lam**(-2)

#-----------Coeficientes obtenidos de Refractiveindex.INFO ---------------------

AireC = [0.05792105,0.00167917, 0,0, 238.0185, 57.362, 0,0]
AguaC = [5.684027565e-1, 1.726177391e-1, 2.086189578e-2, 1.130748688e-1,5.101829712e-3,1.821153936e-2, 2.620722293e-2, 10.69792721 ]
Bk7C = [1.03961212,0.231792344, 1.01046945, 0, 0.00600069867,0.0200179144,103.560653,0  ]
LimeSodaGlassC= [1.5130, 0.003169, 0.003962, 0 , 0, 0 , 0, 0]
Sf10C = [1.62153902, 0.256287842, 1.64447552, 0, 0.0122241457, 0.0595736775, 147.468793, 0 ]
SiC_C = [5.5394,0,0,0, 0.026945,0,0,0]
PmmaC = [1.1819, 0,0 ,0 , 0.011313,0 ,0 ,0 ] 
DiamanteC = [0.3306, 4.3356, 0,0, 0.1750**2 ,0.1060**2,0 ,0 ]

# ------------Definir los materiales -----------------

Aire = Material("Aire", AireC, modelo = 1)
Agua = Material("Agua", AguaC)
BK7 = Material("BK7", Bk7C)
CristalComun = Material("Cristal Común", LimeSodaGlassC, modelo = 2) 
SF10 = Material("SF10", Sf10C)
SiC = Material("SiC", SiC_C)
PMMA = Material("PMMA", PmmaC)
Diamante = Material("Diamante", DiamanteC)
Espejo = Material("Espejo Ideal", None, es_espejo=True)