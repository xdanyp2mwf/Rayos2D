import numpy as np
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection  # Necesario para variar alpha en la línea
from . import Fuentes
from . import Objetos
from . import Materiales as MT

def wavelength_to_rgb(wavelength, gamma=1.0): #Función para convertir longitud de onda a colores RGB
    w = wavelength
    R, G, B = 0.0, 0.0, 0.0
    attenuation = 0.0 

    
    if w >= 0.38 and w < 0.44: # Asignación de Color Base
        R = -(w - 0.44) / (0.44 - 0.38)
        G = 0.05  
        B = 1.0
    elif w >= 0.44 and w < 0.49:
        R = 0.0
        G = (w - 0.44) / (0.49 - 0.44)
        B = 1.0
    elif w >= 0.49 and w < 0.51:
        R = 0.0
        G = 1.0
        B = -(w - 0.51) / (0.51 - 0.49)
    elif w >= 0.51 and w < 0.58:
        R = (w - 0.51) / (0.58 - 0.51)
        G = 1.0
        B = 0.0
    elif w >= 0.58 and w < 0.645:
        R = 1.0
        G = -(w - 0.645) / (0.645 - 0.58)
        B = 0.0
    elif w >= 0.645 and w <= 0.780:
        R = 1.0
        G = 0.0
        B = 0.0
    
    
    elif w < 0.38: # Ultravioleta
        R, G, B = 0.6, 0.0, 1.0 
    elif w > 0.78: # Infrarrojo
        R, G, B = 1.0, 0.0, 0.0 

    
    if 0.38 <= w <= 0.78:
        if w > 0.70:
            attenuation = 0.3 + 0.7 * (0.78 - w) / (0.78 - 0.70)
        

        elif w < 0.40: 
            
            attenuation = 0.5 + 0.5 * (w - 0.38) / (0.40 - 0.38)
        else:
            attenuation = 1.0 
            
    
    elif w < 0.38: # Región UV
       
        attenuation = np.clip(0.8 * (w - 0.20) / (0.38 - 0.20), 0, 0.5)  # Decae suavemente
        
    
    elif w > 0.78: # Región IR
        attenuation = np.clip(0.8 * (1.5 - w) / (1.5 - 0.78), 0, 0.5)

    R *= attenuation
    G *= attenuation
    B *= attenuation
    
    
    return (np.clip(R,0,1)**gamma, np.clip(G,0,1)**gamma, np.clip(B,0,1)**gamma)


class SistemaOptico:
    def __init__(self, objeto, fuente, ambiente=MT.Aire):
        self.objeto = objeto
        self.fuente = fuente
        self.ambiente = ambiente
        self.Historial = None
        self.Historial_Int = None
        self.Lams = None
        self.Ints = None

    def evolucionar(self, pasos=1500, dt=0.008, distMin=0.02, MAX_RAYOS=100000):
        """
        Método encargado de la física.
        pasos: la cantidad de pasos que se propaga el sistema
        dt: cambio del parametro por cada paso 
        disMin: distancia de un rayo a la frontera a la cual detecta la interacción
        MAX_RAYOS: maximo de rayos que se pueden generar (refracciones generan rayos nuevos)
        """        
        Posiciones = self.fuente.r
        Direcciones = self.fuente.k
        LongOnda = self.fuente.lam
        Intensidad = self.fuente.I 

        Frontera = self.objeto.frontera
        Normales = self.objeto.normal 

        cooldownT = np.zeros(Posiciones.shape[0], dtype=int) 
        PasosMuertos = 40  #Para que los rayos no interactuen varias veces (consecutivas) con la misma frontera

        PasosGuardados = 10 #Cada cuantos pasos se guardan las posiciones del rayo y su intensidad
        
        Historial = np.full((pasos // PasosGuardados + 1, MAX_RAYOS, 2), np.nan) # Historial de posiciones e intensidades
        Historial_Int = np.full((pasos // PasosGuardados + 1, MAX_RAYOS), np.nan)
        
        idx_guardado = 0

        def Reflexiones(Rayos, Fronteras):
            PPunto = np.sum(Direcciones[Rayos] * Normales[Fronteras], axis=1)
            k_reflex = Direcciones[Rayos] - 2 * PPunto[:, np.newaxis] * Normales[Fronteras]
            k_reflex /= np.linalg.norm(k_reflex, axis=1, keepdims=True)
            return k_reflex
        
        def Refracciones(Rayos, Fronteras):
            n_ambiente = self.ambiente.n(LongOnda[Rayos])
            n_medio = self.objeto.material.n(LongOnda[Rayos])

            vec_inc = Direcciones[Rayos]
            vec_norm = Normales[Fronteras]

            PPunto = np.sum(vec_inc * vec_norm, axis=1)
            Entrantes = PPunto < 0

            Norm_eff = np.empty_like(vec_norm)
            eta = np.empty(len(Rayos))
            
            
            Norm_eff[Entrantes] = vec_norm[Entrantes] # Entrando 
            eta[Entrantes] = n_ambiente[Entrantes] / n_medio[Entrantes]

            
            Norm_eff[~Entrantes] = -vec_norm[~Entrantes] # Saliendo 
            eta[~Entrantes] = n_medio[~Entrantes] / n_ambiente[~Entrantes]

            
            c1 = -np.sum(vec_inc * Norm_eff, axis=1)
            disc = 1.0 - eta**2 * (1.0 - c1**2)

            R_coef = np.ones(len(Rayos))
            T_coef = np.zeros(len(Rayos))
            no_tir = disc >= 0 #No considerar a los que sufren Reflexión total interna

            if np.any(no_tir):
                c2 = np.sqrt(disc[no_tir])
                eta_v = eta[no_tir]
                c1_v = c1[no_tir]

                rs = ((eta_v * c1_v - c2) / (eta_v * c1_v + c2))
                rp = ((-eta_v * c2 + c1_v) / (eta_v * c2 + c1_v))
                R_coef[no_tir] = 0.5 * (rs**2 + rp**2) #Coeficientes de Fresnell promedio (50% para cada polarización)
                T_coef[no_tir] = 1.0 - R_coef[no_tir]  

            mascara_TIR = no_tir
            if not np.any(mascara_TIR):
                return np.empty((0,2)), np.empty((0,2)), np.array([]), np.array([]), R_coef

            eta_vec = eta[mascara_TIR][:, np.newaxis]
            dir_vec = vec_inc[mascara_TIR]
            N_vec = Norm_eff[mascara_TIR]
            c1_vec = c1[mascara_TIR][:, np.newaxis]
            sqrt_disc_vec = np.sqrt(disc[mascara_TIR])[:, np.newaxis]

            k_refractados = (eta_vec * dir_vec) + ((eta_vec * c1_vec - sqrt_disc_vec) * N_vec)
            k_refractados /= np.linalg.norm(k_refractados, axis=1, keepdims=True)

            r_refractados = Posiciones[Rayos][mascara_TIR]
            lam_refractados = LongOnda[Rayos][mascara_TIR]

            I_refractados = Intensidad[Rayos][mascara_TIR] * T_coef[mascara_TIR] #Los rayos refractados son nuevos rayos


            return k_refractados, r_refractados, lam_refractados, I_refractados, R_coef

        for t in range(pasos):
            N_actual = Posiciones.shape[0]
            if t % PasosGuardados == 0:
                if idx_guardado < len(Historial):
                        Historial[idx_guardado, :N_actual, :] = Posiciones
                        
                        Historial_Int[idx_guardado, :N_actual] = Intensidad
                        idx_guardado += 1
                        print(f"Paso {t} completado. ")

            Posiciones += Direcciones * dt #Se parametriza la propagación de los rayos
            cooldownT = np.maximum(cooldownT-1, 0)

            RayosB_Indices = np.where(cooldownT == 0)[0] #Solo se trabaja con los rayos que no interactuaron recientemente

            if len(RayosB_Indices) == 0: 
                continue

            SubPos = Posiciones[RayosB_Indices]

            dif = SubPos[:, np.newaxis, :] - Frontera[np.newaxis, :, :]
            Distancia = np.sum(dif**2,  axis = 2)

            MascaraChoques = Distancia < distMin**2
            RayosQueChocaron_sub = np.any(MascaraChoques, axis = 1)

            if np.any(RayosQueChocaron_sub): 
                IndicesGlobales_Choque =  RayosB_Indices[RayosQueChocaron_sub] #Se obtiene los indices globales de los rayos que interactuaron
                Indices_Frontera = np.argmax(MascaraChoques[RayosQueChocaron_sub], axis = 1)

                k_t, r_t, L_t, I_t, R_val = Refracciones(IndicesGlobales_Choque, Indices_Frontera) #Se obtienen rayos nuevos
                k_r = Reflexiones(IndicesGlobales_Choque, Indices_Frontera) #Se modifica la dirección de los rayos originales
                
                Direcciones[IndicesGlobales_Choque] = k_r
                Intensidad[IndicesGlobales_Choque] *= R_val

                if N_actual + len(k_t) > MAX_RAYOS:
                    print("Alerta: Máximo de rayos alcanzado, no se generan más refracciones.")
                else:
                    if len(k_t) > 0:
                        Direcciones = np.concatenate((Direcciones, k_t))
                        Posiciones = np.concatenate((Posiciones, r_t))
                        LongOnda = np.concatenate((LongOnda, L_t))
                        Intensidad = np.concatenate((Intensidad, I_t)) 

                        nuevos_cooldowns = np.full(len(k_t), PasosMuertos, dtype=int)
                        cooldownT = np.concatenate((cooldownT, nuevos_cooldowns))
                        cooldownT[IndicesGlobales_Choque] = PasosMuertos #Se identifica qué rayos interactuaron

        Final_Lams = np.full(MAX_RAYOS, np.nan) #Para graficar colores
        Final_Ints = np.zeros(MAX_RAYOS) 
        
        cantidad_final = len(LongOnda)
        Final_Lams[:cantidad_final] = LongOnda
        Final_Ints[:cantidad_final] = Intensidad

        self.Historial = Historial
        self.Historial_Int = Historial_Int
        self.Lams = Final_Lams
        self.Ints = Final_Ints

    def graficar(self):
        """
        Método para graficar despues de ejecutar evolucionar()  
        """
        plt.figure(figsize=(10, 10), facecolor='0.0')  
        ax = plt.gca()
        ax.set_facecolor('0.1') 
        plt.tick_params(axis='both', colors='white')

        PuntosFrontera = self.objeto.frontera
        plt.scatter(PuntosFrontera[:, 0], PuntosFrontera[:, 1],
                    c='black', s=0.05, alpha=0.05)


        Historial = np.transpose(self.Historial, (1, 0, 2))      
        Historial_Int = np.transpose(self.Historial_Int, (1, 0)) 

        for i in range(Historial.shape[0]):
            
            ray_path = Historial[i]
            mask = ~np.isnan(ray_path[:, 0])
            
            
            ray_path = ray_path[mask]
            ray_ints = Historial_Int[i][mask]
            
            if len(ray_path) < 2:
                continue

            
            if np.max(ray_ints) < 0.001: # Filtrar rayos muy débiles
                continue

        
            points = ray_path.reshape(-1, 1, 2)
            segments = np.concatenate([points[:-1], points[1:]], axis=1)

        
            base_rgb = wavelength_to_rgb(self.Lams[i])
            alphas = np.clip(ray_ints[:-1], 0, 1)
            
            colors = np.zeros((len(segments), 4))
            colors[:, 0:3] = base_rgb
            colors[:, 3] = alphas

            lc = LineCollection(segments, colors=colors, linewidth=0.2)
            ax.add_collection(lc)
            
        plt.axis('equal')
        plt.xlim(-10, 10)
        plt.ylim(-10, 10)
        

#-------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------
