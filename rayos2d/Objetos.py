import numpy as np 
import matplotlib.pyplot as plt
from . import Materiales as MT


class Interfaz:
    pass
    def __init__(self,x0,y0,Nx,Ny,material = MT.CristalComun,longitud = 25,num_points=2000): 
        """x0, y0: centro de la interfaz 
        Nx, Ny: vector normal a la interfaz
        material: material del que está hecha la interfaz
        longitud: longitud del interfaz
        num_points: numero de puntos que forman la interfaz
        """
        self.material = material

        vx =  Ny
        vy = -Nx
        magnitud = np.sqrt(vx**2 + vy**2)
        vx = vx / magnitud
        vy = vy / magnitud

        t = np.linspace(-longitud/2, longitud/2, num_points)
        
        x = x0 + (vx * t)
        y = y0 + (vy * t)

        self.frontera = np.array([x,y]).T #Se asignan las coordenadas de la frontera. Transpuesto para que tenga forma (Num_points, 2)

        NorX = np.zeros(num_points) + Nx/magnitud
        NorY = np.zeros(num_points) + Ny/magnitud

        self.normal = np.array([NorX, NorY]).T #Se asigna un vector normal a cada punto de la frontera

    #--------------------------------------------------------------------------------------------------
    #-------------------------------------------------------------------------------------------------


class Rectangulo:
    pass
 
    def __init__(self,x0,y0,A,B,material = MT.CristalComun,Nx = -1 ,Ny = 0 ,num_points=2000):
        """     x0, y0: centro del rectangulo
                A, B: ancho y alto 
                n : Indice de refracción
                Nx, Ny: la normal de la cara izquierda del rectangulo
                material: material del que está hecho el objeto
                num_points: puntos totales del objeto 
        """
        self.material = material
        #--------Frontera--------------
        t1 = np.linspace(0,1,int(num_points/4))
        t2 = np.linspace(1,2,int(num_points/4))
        t3 = np.linspace(2,3,int(num_points/4))
        t4 = np.linspace(3,4,int(num_points/4))


        magnitud = np.sqrt(Nx**2+Ny**2)
        ux =-Nx/magnitud
        uy =-Ny/magnitud

        vx =-uy
        vy = ux

        cx = x0-(A*ux/2)-(B*vx/2)
        cy = y0-(A*uy/2)-(B*vy/2)

        x1 = t1*A*ux
        y1 =  t1*A*uy #Cara inferior

        x2 =  A*ux + (t2-1)*(B*vx)
        y2 = A*uy + (t2-1)*(B*vy) #Cara derecha

        x3 = (A*ux + B*vx) +(t3-2)*(-A*ux)
        y3 = (A*uy + B*vy) +(t3-2)*(-A*uy) #Cara superior

        x4 = (B*vx)+(t4-3)*(-B*vx)
        y4 = (B*vy)+(t4-3)*(-B*vy) #Cara izquierda

        N1x = np.full(int(num_points/4), -vx)
        N1y = np.full(int(num_points/4), -vy)

        N2x = np.full(int(num_points/4), ux)
        N2y = np.full(int(num_points/4), uy)

        N3x = np.full(int(num_points/4), vx)
        N3y = np.full(int(num_points/4), vy)

        N4x = np.full(int(num_points/4), -ux)
        N4y = np.full(int(num_points/4), -uy) #Normales de las caras
        
        x = np.concatenate((x1, x2, x3, x4))
        y = np.concatenate((y1, y2, y3, y4))

        NorX = np.concatenate((N1x,N2x, N3x, N4x))
        NorY = np.concatenate((N1y,N2y, N3y, N4y))
        

        self.frontera = np.array([x + cx,y + cy]).T 
        self.normal = np.array([NorX, NorY]).T

    #--------------------------------------------------------------------------------------------------
    #-------------------------------------------------------------------------------------------------

class TrianguloEquilatero:
    pass

    def __init__(self, x0, y0, L, material = MT.CristalComun, Nx=0, Ny=1, num_points=2000):
        """
        x0, y0: centro del triangulo
        L : Largo de los lados
        material: material del que está hecho el objeto
        Nx, Ny, dirección del centro al vertice superior
        num_points = numero de puntos que forman la frontera
        """

        self.material = material
        
        
        R = L / np.sqrt(3)  
        norm = np.sqrt(Nx**2 + Ny**2)
        ux, uy = Nx/norm, Ny/norm
        
        sin120 = np.sqrt(3) / 2
        cos120 = -0.5

        
        v1 = np.array([ux * R, uy * R]) #vertices
        
        
        v2_x = v1[0] * cos120 - v1[1] * sin120
        v2_y = v1[0] * sin120 + v1[1] * cos120
        v2 = np.array([v2_x, v2_y])
        
        
        v3_x = v2[0] * cos120 - v2[1] * sin120
        v3_y = v2[0] * sin120 + v2[1] * cos120
        v3 = np.array([v3_x, v3_y])

        P1 = v1 + [x0, y0]
        P2 = v2 + [x0, y0]
        P3 = v3 + [x0, y0]

        
        N_side = int(num_points / 3)
        t = np.linspace(0, 1, N_side)

        
        x_s1 = P2[0] + t * (P3[0] - P2[0]) #Parametrización de los lados
        y_s1 = P2[1] + t * (P3[1] - P2[1])

        
        x_s2 = P3[0] + t * (P1[0] - P3[0])
        y_s2 = P3[1] + t * (P1[1] - P3[1])

        
        x_s3 = P1[0] + t * (P2[0] - P1[0])
        y_s3 = P1[1] + t * (P2[1] - P1[1])

        
        def normal(inicio, final, cuenta):
            dx = final[0] - inicio[0]
            dy = final[1] - inicio[1]
            nm = np.sqrt(dx**2 + dy**2) 
            
            return np.full(cuenta, dy/nm), np.full(cuenta, -dx/nm)

        nx1, ny1 = normal(P2, P3, N_side)
        nx2, ny2 = normal(P3, P1, N_side)
        nx3, ny3 = normal(P1, P2, N_side)

        
        self.frontera = np.array([
            np.concatenate((x_s1, x_s2, x_s3)),
            np.concatenate((y_s1, y_s2, y_s3))
        ]).T
        
        self.normal = np.array([
            np.concatenate((nx1, nx2, nx3)),
            np.concatenate((ny1, ny2, ny3))
        ]).T     
    #--------------------------------------------------------------------------------------------------
    #-------------------------------------------------------------------------------------------------


class Lente:
    def __init__(self, x0, y0, R1, R2, grosor, apertura, material=MT.CristalComun, Nx=0, Ny=1, num_puntos=2000):
        """
        x0, y0: centro del lente
        R1, R2: radios de curvatura (+) apunta hacia izquierda, (-) apunta hacia derecha
        grosor: grosor de la lente
        Apertura: alto de la lente
        material: material del que está hecho el objeto 
        Nx, Ny: dirección del centro a la tapa superior
        num_puntos: numero de puntos que forman la frontera del objeto

        """
        self.material = material
        
        
        norm = np.sqrt(Nx**2 + Ny**2)  # Vectores Base de rotación
        if norm == 0: norm = 1
        ux, uy = Nx/norm, Ny/norm
        v_arr = np.array([ux, uy])      
        v_der = np.array([uy, -ux])     

       
        x_v1 = -grosor / 2  
        x_v2 = grosor / 2   
        h = apertura / 2.0

        # --- FUNCIONES AUXILIARES  ---
        
        def get_arc_params(R, h_apert):
            """Retorna longitud de arco y rango de ángulos para un radio y apertura dados."""
            if np.isinf(R):
                return 2 * h_apert, None # Longitud es la altura recta
            
            
            ratio = np.clip(h_apert / np.abs(R), -1.0, 1.0)
            theta_max = np.arcsin(ratio)
            
            length = np.abs(R) * (2 * theta_max)
            return length, theta_max

        def generar_arco(R, x_vertice, n_pts, es_cara_izq):
            """Genera x, y, nx, ny usando distribución angular."""
            if n_pts < 2: n_pts = 2
            
            
            if np.isinf(R): # CASO PLANO 
                y = np.linspace(-h, h, n_pts)
                x = np.full_like(y, x_vertice)
                nx_val = -1 if es_cara_izq else 1
                return x, y, np.full_like(y, nx_val), np.zeros_like(y)

            
            ratio = np.clip(h / np.abs(R), -1.0, 1.0) # CASO CURVO 
            theta_max = np.arcsin(ratio)
            
           
            thetas = np.linspace(-theta_max, theta_max, n_pts)
            
            
            cx = x_vertice + R
            
            sign_r = np.sign(R)
            abs_r = np.abs(R)
            
            
            dx = -sign_r * abs_r * np.cos(thetas)
            dy = abs_r * np.sin(thetas) # y va de -h a h
            
            x = cx + dx
            y = dy # Centrado en 0
            

            nx = dx / abs_r # Normalizado
            ny = dy / abs_r 
            
            if es_cara_izq:
               
                if np.mean(nx) > 0: nx *= -1; ny *= -1
            else:
            
                if np.mean(nx) < 0: nx *= -1; ny *= -1
                
            return x, y, nx, ny

        
        len_der, ang_der = get_arc_params(R2, h)
        len_izq, ang_izq = get_arc_params(R1, h)

        
        
        if np.isinf(R2): x_der_top = x_v2 # Borde superior derecha
        else: x_der_top = (x_v2 + R2) - np.sign(R2)*np.sqrt(R2**2 - h**2)
        
        
        if np.isinf(R1): x_izq_top = x_v1 # Borde superior izquierda
        else: x_izq_top = (x_v1 + R1) - np.sign(R1)*np.sqrt(R1**2 - h**2)

        
        dist_x_tapa = x_izq_top - x_der_top # La longitud de la tapa
       
        len_tapa = np.abs(dist_x_tapa) 
        
        perimetro_total = len_der + len_izq + 2 * len_tapa
        if perimetro_total == 0: perimetro_total = 1 

        
        n_der = int(num_puntos * (len_der / perimetro_total))
        n_izq = int(num_puntos * (len_izq / perimetro_total))
        n_tapa = int(num_puntos * (len_tapa / perimetro_total))
        
        #
        if n_der < 2: n_der = 2
        if n_izq < 2: n_izq = 2

        if len_tapa > 1e-5 and n_tapa < 2: n_tapa = 2
        elif len_tapa <= 1e-5: n_tapa = 0 # Lente cerrada (círculo perfecto o intersección)

     
        
        
        x_d, y_d, nx_d, ny_d = generar_arco(R2, x_v2, n_der, False) # Cara Derecha (R2)

        
        x_i, y_i, nx_i, ny_i = generar_arco(R1, x_v1, n_izq, True) # Cara Izquierda (R1) 
        
        x_i = np.flip(x_i)
        y_i = np.flip(y_i)
        nx_i = np.flip(nx_i)
        ny_i = np.flip(ny_i)

       

        if n_tapa > 0:  # Tapas 
            x_sup = np.linspace(x_d[-1], x_i[0], n_tapa)
            y_sup = np.linspace(y_d[-1], y_i[0], n_tapa)
            nx_sup = np.zeros(n_tapa)
            ny_sup = np.ones(n_tapa) 

            x_inf = np.linspace(x_i[-1], x_d[0], n_tapa)
            y_inf = np.linspace(y_i[-1], y_d[0], n_tapa)
            nx_inf = np.zeros(n_tapa)
            ny_inf = np.full(n_tapa, -1.0) 
        else:
            
            x_sup, y_sup, nx_sup, ny_sup = [], [], [], []
            x_inf, y_inf, nx_inf, ny_inf = [], [], [], []

        
        x_loc = np.concatenate((x_d, x_sup, x_i, x_inf))
        y_loc = np.concatenate((y_d, y_sup, y_i, y_inf))
        nx_loc = np.concatenate((nx_d, nx_sup, nx_i, nx_inf))
        ny_loc = np.concatenate((ny_d, ny_sup, ny_i, ny_inf))

        
        self.frontera = np.array([
            x0 + x_loc * v_der[0] + y_loc * v_arr[0],
            y0 + x_loc * v_der[1] + y_loc * v_arr[1]
        ]).T
        
        self.normal = np.array([
            nx_loc * v_der[0] + ny_loc * v_arr[0],
            nx_loc * v_der[1] + ny_loc * v_arr[1]
        ]).T


class Corazon:
    def __init__(self, x0, y0, escala=1.0, material=MT.CristalComun, num_puntos=2000):
        """
        x0, y0: Centro del corazón
        escala: Tamaño del objeto
        material: Material óptico
        num_puntos: Resolución de la frontera
        """
        self.material = material
        
        
        t = np.linspace(0, 2 * np.pi, num_puntos)
        
        
        x_local = 16 * np.sin(t)**3
        y_local = 13 * np.cos(t) - 5 * np.cos(2*t) - 2 * np.cos(3*t) - np.cos(4*t)
        
        
        x = x0 + (x_local * escala / 16)
        y = y0 + (y_local * escala / 16)
        
        self.frontera = np.array([x, y]).T
        
        
        dx = 48 * np.sin(t)**2 * np.cos(t)
        dy = -13 * np.sin(t) + 10 * np.sin(2*t) + 6 * np.sin(3*t) + 4 * np.sin(4*t)
        
        
        norma = np.sqrt(dx**2 + dy**2)
        norma[norma == 0] = 1e-9 # Evita NaN reemplazando 0 con un valor minúsculo
        
        nx = -dy / norma
        ny = dx / norma
        
        self.normal = np.array([nx, ny]).T
    #--------------------------------------------------------------------------------------------------
    #--------------------------------------------------------------------------------------------------


def graficar_lente(ax, lente, titulo):

    x_plot = np.append(lente.frontera.T[0], lente.frontera.T[0][0])
    y_plot = np.append(lente.frontera.T[1], lente.frontera.T[1][0])
    
    ax.plot(x_plot, y_plot, 'b-', linewidth=2, label='Superficie')
    ax.fill(x_plot, y_plot, 'cyan', alpha=0.3) 


    salto = 40 
    
    x_quiv = lente.frontera.T[0][::salto]
    y_quiv = lente.frontera.T[1][::salto]
    nx_quiv = lente.normal.T[0][::salto]
    ny_quiv = lente.normal.T[1][::salto]

   
    ax.quiver(x_quiv, y_quiv, nx_quiv, ny_quiv, color='red', scale=25, width=0.005, label='Normales')

    
    ax.set_aspect('equal', 'box') # 
    ax.grid(True, linestyle='--')
    ax.axhline(0, color='black', lw=0.5)
    ax.axvline(0, color='black', lw=0.5)
    ax.set_title(titulo)



# --- Creación de Ejemplos ---
"""
# Figuras para mostrar distintos casos
fig, axes = plt.subplots(4, 2, figsize=(12, 10))
axes = axes.flatten()

# Caso 1: Biconvexa Estándar (R1+, R2-)
lente1 = Lente(x0=0, y0=0, R1=50, R2=-50, grosor=5, apertura=10)
graficar_lente(axes[0], lente1, "1. Biconvexa (R1=50, R2=-50)")

# Caso 2: Plano-Cóncava (R1=inf, R2+)
# R2 positivo significa centro a la derecha -> cara derecha es cóncava
lente2 = Lente(x0=0, y0=0, R1=np.inf, R2=30, grosor=5, apertura=10)
graficar_lente(axes[1], lente2, "2. Plano-Cóncava (R1=inf, R2=30)")

# Caso 3: Menisco Positivo (R1+, R2+, R1 < R2)
# Ambas curvas hacia la derecha, pero la izq es más cerrada
lente3 = Lente(x0=0, y0=0, R1=20, R2=40, grosor=5, apertura=10)
graficar_lente(axes[2], lente3, "3. Menisco (R1=20, R2=40)")

# Caso 4: Biconvexa Rotada e inclinada
lente4 = Lente(x0=10, y0=10, R1=60, R2=-60, grosor=5, apertura=10, Ny=2)
graficar_lente(axes[3], lente4, "4. Rotada (vec_arriba=(1,2))")

LenteBiconvexa = Lente(0, 0, -3, 3, 2, 5 )
graficar_lente(axes[4], LenteBiconvexa, "5. Lente biconvexa")

prisma = TrianguloEquilatero( 6 , 0 , 3 ,Nx =0)
graficar_lente(axes[5], prisma, "6.  prisma equilatero")

Vidrio = Rectangulo(0, 0, 5, 10,  Ny= 8)
graficar_lente(axes[6], Vidrio, "Lente plano ")

Agua = Interfaz( 0 , 0 , 1,6, material= MT.Agua)
graficar_lente(axes[7], Agua, "Interfaz ")

# Añadir leyenda solo al primer plot para no saturar
axes[0].legend()
for i in range(0,8):
    axes[i].set_xlim(-10,10)
    axes[i].set_ylim(-10,10)

plt.tight_layout()
plt.show()"""

