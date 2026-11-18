import numpy as np
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection  # Necesario para variar alpha en la línea
from . import Fuentes
from . import Objetos
from . import Materiales as MT

# --- Función de Color ---
def wavelength_to_rgb(wavelength, gamma=1.0): 
    w = wavelength; R, G, B = 0.0, 0.0, 0.0; attenuation = 0.0 
    if w >= 0.38 and w < 0.44: R = -(w - 0.44) / (0.44 - 0.38); G = 0.05; B = 1.0
    elif w >= 0.44 and w < 0.49: R = 0.0; G = (w - 0.44) / (0.49 - 0.44); B = 1.0
    elif w >= 0.49 and w < 0.51: R = 0.0; G = 1.0; B = -(w - 0.51) / (0.51 - 0.49)
    elif w >= 0.51 and w < 0.58: R = (w - 0.51) / (0.58 - 0.51); G = 1.0; B = 0.0
    elif w >= 0.58 and w < 0.645: R = 1.0; G = -(w - 0.645) / (0.645 - 0.58); B = 0.0
    elif w >= 0.645 and w <= 0.780: R = 1.0; G = 0.0; B = 0.0
    elif w < 0.38: R, G, B = 0.6, 0.0, 1.0 
    elif w > 0.78: R, G, B = 1.0, 0.0, 0.0 
    if 0.38 <= w <= 0.78:
        if w > 0.70: attenuation = 0.3 + 0.7 * (0.78 - w) / (0.78 - 0.70)
        elif w < 0.40: attenuation = 0.5 + 0.5 * (w - 0.38) / (0.40 - 0.38)
        else: attenuation = 1.0 
    elif w < 0.38: attenuation = np.clip(0.8 * (w - 0.20) / (0.38 - 0.20), 0, 0.5)
    elif w > 0.78: attenuation = np.clip(0.8 * (1.5 - w) / (1.5 - 0.78), 0, 0.5)
    R *= attenuation; G *= attenuation; B *= attenuation
    return (np.clip(R,0,1)**gamma, np.clip(G,0,1)**gamma, np.clip(B,0,1)**gamma)

# --- Clase Sistema ---
class SistemaOptico:
    def __init__(self, objetos, fuente, ambiente=MT.Aire):
        if isinstance(objetos, list):
            self.objetos = objetos
        else:
            self.objetos = [objetos]
            
        self.fuente = fuente
        self.ambiente = ambiente
        self.Historial = None
        self.Historial_Int = None
        self.Lams = None
        self.Ints = None
        self.FronteraGlobal = None
        self.NormalesGlobal = None
        self.MapIDMaterial = None 

    def evolucionar(self, pasos=1500, dt=0.008, distMin=0.02, MAX_RAYOS=100000, min_int=0.01):
        # Pre-procesamiento de geometría
        lista_puntos = []
        lista_normales = []
        lista_ids = []

        for i, obj in enumerate(self.objetos):
            pts = obj.frontera
            norms = obj.normal
            lista_puntos.append(pts)
            lista_normales.append(norms)
            lista_ids.append(np.full(len(pts), i, dtype=int))

        self.FronteraGlobal = np.vstack(lista_puntos)
        self.NormalesGlobal = np.vstack(lista_normales)
        self.MapIDMaterial = np.concatenate(lista_ids)

        Posiciones = self.fuente.r
        Direcciones = self.fuente.k
        LongOnda = self.fuente.lam
        Intensidad = self.fuente.I 

        Frontera = self.FronteraGlobal
        Normales = self.NormalesGlobal
        
        cooldownT = np.zeros(Posiciones.shape[0], dtype=int) 
        PasosMuertos = 20  
        PasosGuardados = 10
        
        Historial = np.full((pasos // PasosGuardados + 1, MAX_RAYOS, 2), np.nan) 
        Historial_Int = np.full((pasos // PasosGuardados + 1, MAX_RAYOS), np.nan)
        idx_guardado = 0

        # Funciones físicas internas
        def Reflexiones(Rayos, Fronteras):
            PPunto = np.sum(Direcciones[Rayos] * Normales[Fronteras], axis=1)
            k_reflex = Direcciones[Rayos] - 2 * PPunto[:, np.newaxis] * Normales[Fronteras]
            k_reflex /= np.linalg.norm(k_reflex, axis=1, keepdims=True)
            return k_reflex
        
        def Refracciones(Rayos, Indices_Puntos_Impacto):
            n_ambiente = self.ambiente.n(LongOnda[Rayos])
            IDs_Objetos_Golpeados = self.MapIDMaterial[Indices_Puntos_Impacto]
            mask_espejos = np.zeros(len(Rayos), dtype=bool)
            n_medio = np.zeros(len(Rayos))
            unique_obj_ids = np.unique(IDs_Objetos_Golpeados)
            for obj_id in unique_obj_ids:
                mask = (IDs_Objetos_Golpeados == obj_id)
                material_obj = self.objetos[obj_id].material
                if material_obj.es_espejo: mask_espejos[mask] = True
                else: n_medio[mask] = material_obj.n(LongOnda[Rayos][mask])

            R_coef = np.zeros(len(Rayos)); T_coef = np.zeros(len(Rayos))
            if np.any(mask_espejos): R_coef[mask_espejos] = 1.0; T_coef[mask_espejos] = 0.0
            mask_diel = ~mask_espejos
            
            if np.any(mask_diel):
                idx = np.where(mask_diel)[0]
                v_i = Direcciones[Rayos][idx]; v_n = Normales[Indices_Puntos_Impacto][idx]
                n1 = n_ambiente[idx]; n2 = n_medio[idx]
                PP = np.sum(v_i * v_n, axis=1); Ent = PP < 0
                Ne = np.where(Ent[:,None], v_n, -v_n); et = np.where(Ent, n1/n2, n2/n1)
                c1 = -np.sum(v_i * Ne, axis=1); disc = 1.0 - et**2 * (1.0 - c1**2)
                R_s = np.ones(len(idx)); ntir = disc >= 0
                if np.any(ntir):
                    c2 = np.sqrt(disc[ntir]); et_v = et[ntir]; c1_v = c1[ntir]
                    rs = (et_v*c1_v - c2)/(et_v*c1_v + c2); rp = (-et_v*c2 + c1_v)/(et_v*c2 + c1_v)
                    R_s[ntir] = 0.5*(rs**2 + rp**2)
                R_coef[idx] = R_s; T_coef[idx] = 1.0 - R_s

            mask_T = (T_coef > 0.001)
            if not np.any(mask_T): return np.empty((0,2)), np.empty((0,2)), [], [], R_coef

            idx_t = np.where(mask_T)[0]
            v_i_t = Direcciones[Rayos][idx_t]; v_n_t = Normales[Indices_Puntos_Impacto][idx_t]
            n1_t = n_ambiente[idx_t]; n2_t = n_medio[idx_t]
            PP_t = np.sum(v_i_t * v_n_t, axis=1); Ent_t = PP_t < 0
            Ne_t = np.where(Ent_t[:,None], v_n_t, -v_n_t); et_t = np.where(Ent_t, n1_t/n2_t, n2_t/n1_t)
            c1_t = -np.sum(v_i_t * Ne_t, axis=1); disc_t = 1.0 - et_t**2 * (1.0 - c1_t**2)
            
            sq_d = np.sqrt(np.maximum(0, disc_t))[:,None]; et_v = et_t[:,None]; c1_v = c1_t[:,None]
            k_t = (et_v * v_i_t) + ((et_v * c1_v - sq_d) * Ne_t)
            k_t /= np.linalg.norm(k_t, axis=1, keepdims=True)
            
            return k_t, Posiciones[Rayos][idx_t], LongOnda[Rayos][idx_t], Intensidad[Rayos][idx_t]*T_coef[idx_t], R_coef

        # --- BUCLE PRINCIPAL ---
        print(f"Iniciando simulación de {pasos} pasos...")
        
        for t in range(pasos):
            N_actual = Posiciones.shape[0]
            
            # OPTIMIZACIÓN 1: Máscara de vida
            MascaraVivos = Intensidad > min_int

            # Feedback visual simple (sin librerías extra)
            if t % (pasos // 10) == 0:
                print(f"Progreso: {int(t/pasos*100)}% | Rayos vivos: {np.sum(MascaraVivos)}")

            if t % PasosGuardados == 0:
                if idx_guardado < len(Historial):
                        Historial[idx_guardado, :N_actual, :] = Posiciones
                        Historial_Int[idx_guardado, :N_actual] = Intensidad
                        idx_guardado += 1

            # OPTIMIZACIÓN 2: Movimiento selectivo
            if np.any(MascaraVivos):
                Posiciones[MascaraVivos] += Direcciones[MascaraVivos] * dt 
                cooldownT[MascaraVivos] = np.maximum(cooldownT[MascaraVivos]-1, 0)
            else:
                # Si todos se apagan, terminamos antes
                print("Todos los rayos se han extinguido.")
                break

            # OPTIMIZACIÓN 3: Choques selectivos
            RayosB_Indices = np.where(MascaraVivos & (cooldownT == 0))[0] 
            
            if len(RayosB_Indices) == 0: continue

            SubPos = Posiciones[RayosB_Indices]
            dif = SubPos[:, np.newaxis, :] - Frontera[np.newaxis, :, :]
            Distancia = np.sum(dif**2,  axis = 2)

            MascaraChoques = Distancia < distMin**2
            if np.any(MascaraChoques):
                RayosQueChocaron_sub = np.any(MascaraChoques, axis = 1)
                IndicesGlobales_Choque = RayosB_Indices[RayosQueChocaron_sub] 
                
                if len(IndicesGlobales_Choque) > 0:
                    Indices_Frontera = np.argmax(MascaraChoques[RayosQueChocaron_sub], axis = 1)

                    k_t, r_t, L_t, I_t, R_val = Refracciones(IndicesGlobales_Choque, Indices_Frontera)
                    k_r = Reflexiones(IndicesGlobales_Choque, Indices_Frontera) 
                    
                    Direcciones[IndicesGlobales_Choque] = k_r
                    Intensidad[IndicesGlobales_Choque] *= R_val

                    if len(k_t) > 0:
                        if N_actual + len(k_t) <= MAX_RAYOS:
                            Direcciones = np.concatenate((Direcciones, k_t))
                            Posiciones = np.concatenate((Posiciones, r_t))
                            LongOnda = np.concatenate((LongOnda, L_t))
                            Intensidad = np.concatenate((Intensidad, I_t)) 
                            
                            nuevos_cooldowns = np.full(len(k_t), PasosMuertos, dtype=int)
                            cooldownT = np.concatenate((cooldownT, nuevos_cooldowns))
                        else:
                            print("Aviso: Máximo de rayos alcanzado.")

                    cooldownT[IndicesGlobales_Choque] = PasosMuertos 

        # Guardado final
        print("Simulación finalizada. Procesando datos...")
        Final_Lams = np.full(MAX_RAYOS, np.nan) 
        Final_Ints = np.zeros(MAX_RAYOS) 
        n = len(LongOnda)
        Final_Lams[:n] = LongOnda; Final_Ints[:n] = Intensidad
        self.Historial = Historial; self.Historial_Int = Historial_Int
        self.Lams = Final_Lams; self.Ints = Final_Ints

    def graficar(self):
        plt.figure(figsize=(10, 10), facecolor='0.0')  
        ax = plt.gca(); ax.set_facecolor('0.1') 
        plt.tick_params(axis='both', colors='white')

        for obj in self.objetos:
            PuntosFrontera = obj.frontera
            color_obj = 'cyan' if obj.material.es_espejo else 'white'
            alpha_obj = 0.1 if obj.material.es_espejo else 0.1
            plt.scatter(PuntosFrontera[:, 0], PuntosFrontera[:, 1],
                        c=color_obj, s=0.005, alpha=alpha_obj)

        Historial = np.transpose(self.Historial, (1, 0, 2))      
        Historial_Int = np.transpose(self.Historial_Int, (1, 0)) 

        print("Generando gráfico...")
        for i in range(Historial.shape[0]):
            ray_path = Historial[i]
            mask = ~np.isnan(ray_path[:, 0])
            ray_path = ray_path[mask]
            ray_ints = Historial_Int[i][mask]
            
            # Filtro gráfico adicional: no dibujar trazos invisibles
            if len(ray_path) < 2: continue
            if np.max(ray_ints) < 0.001: continue

            points = ray_path.reshape(-1, 1, 2)
            segments = np.concatenate([points[:-1], points[1:]], axis=1)
            base_rgb = wavelength_to_rgb(self.Lams[i])
            alphas = np.clip(ray_ints[:-1], 0, 1)
            colors = np.zeros((len(segments), 4))
            colors[:, 0:3] = base_rgb; colors[:, 3] = alphas

            lc = LineCollection(segments, colors=colors, linewidth=0.2)
            ax.add_collection(lc)
            
        plt.axis('equal'); plt.xlim(-15, 15); plt.ylim(-15, 15)

#-------------------------------------------------------------------------------------------------------------------------
