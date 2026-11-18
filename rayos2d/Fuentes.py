import numpy as np


class Fuentes:
    def __init__(self, r, k, lam):
            """
            Constructor base (interno).
            Recibe los arrays ya calculados. La intensidad se inicializa siempre a 1.
            """
            self.r = np.atleast_2d(r).astype(np.float64)
            k_raw = np.atleast_2d(k).astype(np.float64)
            self.N = self.r.shape[0]

           
            norm_k = np.linalg.norm(k_raw, axis=1, keepdims=True)
            norm_k[norm_k == 0] = 1.0 
            self.k = k_raw / norm_k

            self.lam = np.array(lam, dtype=np.float64)
            
            
            self.I = np.ones(self.N, dtype=np.float64) # Intensidad inicial de 1.0 para todos los rayos


    @staticmethod
    def _calcular_lambdas(N, centro, ancho, tipo_dist):
            """
            Genera el array de lambdas según la distribución elegida.
            El primer elemento siempre es igual al valor central.
            """
            lams = np.empty(N, dtype=np.float64)

            if tipo_dist == 'monocromatica':
                lams = np.full(N, centro, dtype=np.float64)
            
            elif tipo_dist == 'gaussiana':
                
                lams = np.random.normal(loc=centro, scale=ancho, size=N)
            
            elif tipo_dist == 'uniforme':
                
                lams = np.random.uniform(low=centro - ancho, high=centro + ancho, size=N)
            
            else:
                
                print(f"Aviso: Distribución '{tipo_dist}' no reconocida. Usando monocromática.")
                lams = np.full(N, centro, dtype=np.float64)

            if N > 0:
                lams[0] = centro
                
            return lams

    @classmethod
    def fuente_puntual(cls, origen, N, angulo_apertura=360, 
                        lam=0.55, lam_ancho=0.0, lam_dist='monocromatica'):
            """
            origen: coordenada de donde salen los rayos (x, y)
            N: numero de rayos que se generan inicialmente
            angulo_apertura: Grados del cono de emisión (360 = todo alrededor).
            lam: centro de la distribución de longitudes de onda (en micrometros)
            lam_ancho: ancho de la distribución (en micrometros)
            lam_dist: Distribución de las longitudes de onda 'monocromatica', 'gaussiana', 'uniforme'
            """
            
            r = np.tile(origen, (N, 1))

            
            apertura_rad = np.deg2rad(angulo_apertura)
            theta = np.random.uniform(-apertura_rad/2, apertura_rad/2, N)
            k = np.column_stack((np.cos(theta), np.sin(theta)))

            lams = cls._calcular_lambdas(N, lam, lam_ancho, lam_dist)

            return cls(r, k, lams)
    
    @classmethod
    def haz_colimado(cls, centro, ancho_haz, direccion, N, 
                        lam=0.55, lam_ancho=0.0, lam_dist='monocromatica'):
            """
            centro: coordenada del centro de donde salen los rayos (x, y)
            ancho_haz: ancho desde el cual se generan los rayos
            dirección: dirección hacia donde se dirigen los rayos (i_x, i_y)
            N: cantidad de rayos que se generan
            lam: centro de la distribución de longitudes de onda (en micrometros)
            lam_ancho: ancho de la distribución (en micrometros)
            lam_dist: Distribución de las longitudes de onda 'monocromatica', 'gaussiana', 'uniforme'
            """
            
            d = np.array(direccion, dtype=np.float64)
            d /= np.linalg.norm(d)
            k = np.tile(d, (N, 1))

            
            perp = np.array([-d[1], d[0]])
            offsets = np.random.uniform(-ancho_haz/2, ancho_haz/2, N)
            r = centro + offsets[:, np.newaxis] * perp

            
            lams = cls._calcular_lambdas(N, lam, lam_ancho, lam_dist)

            return cls(r, k, lams)


