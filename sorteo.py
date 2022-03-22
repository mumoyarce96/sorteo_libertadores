import numpy as np
import pandas as pd
from random import randint

class Equipo:
    def __init__(self, nombre, pais, bombo):
        self.nombre = nombre
        self.pais = pais
        self.bombo = bombo
        self.grupo = ''
        
        return
    
class Grupo:
    def __init__(self, nombre):
        self.nombre = nombre
        self.equipos = []
            
    def nuevo_equipo(self, equipo):
        self.equipos.append(equipo)
        return
    
    def tiene_equipo_pais(self, pais):
        for equipo in self.equipos:
            if equipo.pais == pais:
                return True
        return False
    
    def esta_ocupado(self, bombo, pais):
        if self.tiene_equipo_pais(pais) or len(self.equipos) >= bombo.numero:
            return True
        return False

class Bombo():
    def __init__(self, numero, equipos):
        self.numero = numero
        self.equipos = equipos
        
    def contar_grupos_posibles(self, grupos, pais):
        condicion = [grupo.esta_ocupado(self, pais) for grupo in grupos]
        grupos_sin_pais = len(grupos) - sum(condicion)
        return grupos_sin_pais


    def condiciones_pais(self, grupos, grupo, equipo, pais):
        en_bombo = self.contar_equipos_pais(pais)
        grupos_posibles = self.contar_grupos_posibles(grupos, pais)
        cupos_disponibles = grupos_posibles  - en_bombo
        condiciones = cupos_disponibles == 0 and equipo.pais != pais and grupo.tiene_equipo_pais(pais) == False 
        return condiciones

    def numero_de_equipos(self):
        return len(self.equipos)
    
    def quitar_equipo(self, index):
        self.equipos.pop(index)
        return
    
    def contar_equipos_pais(self, pais):
        condicion = [equipo.pais == pais for equipo in self.equipos]
        conteo = sum(condicion)
        return conteo
    
    def ubicar_equipo(self, grupos, index_grupo, nuevo_equipo):
        grupo = grupos[index_grupo]
        for equipo in grupo.equipos:        
            if equipo.pais == nuevo_equipo.pais:
                self.ubicar_equipo(grupos, index_grupo + 1, nuevo_equipo)
                return
    
        condiciones_brasil = self.condiciones_pais(grupos, grupo, nuevo_equipo, 'Brasil')
        condiciones_argentina = self.condiciones_pais(grupos, grupo, nuevo_equipo, 'Argentina')
        if (condiciones_brasil or condiciones_argentina) and len(self.equipos) > 1:
            self.ubicar_equipo(grupos, index_grupo + 1, nuevo_equipo)
            return         
        else:
            grupo.nuevo_equipo(nuevo_equipo)
            nuevo_equipo.grupo = grupo.nombre
            grupos.pop(index_grupo) 
            return 
    
    def sortear(self, grupos):
        grupos_aux = grupos.copy()
        n = len(grupos_aux)
        if self.numero != 1:        
            while n > 0:
                index = randint(0, self.numero_de_equipos() - 1)
                nuevo_equipo = self.equipos[index]
                self.ubicar_equipo(grupos_aux, 0, nuevo_equipo)
                self.quitar_equipo(index) #sacar equipo del bombo
                n = len(grupos_aux)
        else: 
            while n > 1:
                index = randint(0, self.numero_de_equipos() - 1)
                nuevo_equipo = self.equipos[index]
                self.ubicar_equipo(grupos_aux, 1, nuevo_equipo)
                self.quitar_equipo(index) #sacar equipo del bombo
                n = len(grupos_aux)    
        return

# Brasil
PAL = Equipo('Palmeiras', 'Brasil', 1)
AP = Equipo('Athletico Paranaense', 'Brasil', 1)
CAM = Equipo('Atlético Mineiro', 'Brasil', 1)
FLA = Equipo('Flamengo', 'Brasil', 1)
FOR = Equipo('Fortaleza', 'Brasil', 4)
COR = Equipo('Corinthians', 'Brasil', 2)
RBB = Equipo('Bragantino', 'Brasil', 3)

# Argentina
COL = Equipo('Colón', 'Argentina', 3)
RIV = Equipo('River Plate', 'Argentina', 1)
BOC = Equipo('Boca Juniors', 'Argentina', 1)
VEL = Equipo('Vélez', 'Argentina', 2)
TAL = Equipo('Talleres', 'Argentina', 4)

# Bolivia 
IP = Equipo('Independiente Petrolero', 'Bolivia', 4)
AR = Equipo('Always Ready', 'Bolivia', 4)

# Chile
UC = Equipo('Universidad Católica', 'Chile', 2)
CC = Equipo('Colo Colo', 'Chile', 2)

# Colombia 
TOL = Equipo('Deportes Tolima', 'Colombia', 3)
CAL = Equipo('Deportivo Cali', 'Colombia', 3)

# Ecuador
IDV = Equipo('Independiente del Valle', 'Ecuador', 2)
EME = Equipo('Emelec', 'Ecuador', 2)

# Paraguay
CP = Equipo('Cerro Porteño', 'Paraguay', 2)
LIB = Equipo('Libertad', 'Paraguay', 2)

# Perú
AL = Equipo('Alianza Lima', 'Perú', 3)
SC = Equipo('Sporting Cristal', 'Perú', 3)

# Uruguay
PEN = Equipo('Peñarol', 'Uruguay', 1)
NAC = Equipo('Nacional', 'Uruguay', 1)

# Venezuela
DT = Equipo('Deportivo Táchira', 'Venezuela', 3)
CAR = Equipo('Caracas', 'Venezuela', 3)

# Fase Previa
G1 = Equipo('Olimpia', 'Fase previa', 4)
G2 = Equipo('Estudiantes L.P.', 'Fase previa', 4)
G3 = Equipo('The Strongest', 'Fase previa', 4)
G4 = Equipo('América M.G.', 'Fase previa', 4)

equipos = [PAL, RIV, BOC, FLA, NAC, PEN, CAM, CP, AP, LIB, IDV, UC, EME, COR, CC, 
           VEL, SC, CAL, RBB, DT, AL, COL, TOL, CAR, AR, TAL, IP, FOR, G1, G2, G3, G4]


# Bombos
equipos_por_bombo = [[equipo for equipo in equipos if equipo.bombo == i] for i in range(1,5)]  
bombos = [Bombo(i+1, equipos_por_bombo[i]) for i in range(len(equipos_por_bombo))]

# Dataframe
bombos_df = pd.DataFrame({'Bolillero 1': [equipo.nombre for equipo in equipos_por_bombo[0]],
                   'Bolillero 2': [equipo.nombre for equipo in equipos_por_bombo[1]],
                   'Bolillero 3': [equipo.nombre for equipo in equipos_por_bombo[2]],
                   'Bolillero 4': [equipo.nombre for equipo in equipos_por_bombo[3]],})
tablas = [bombos_df.to_html(classes='bombos', index = False)]
titulos = bombos_df.columns.values


# Sorteo
def sortear():
    nombres = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
    grupos = [Grupo(nombre) for nombre in nombres]
    equipos_por_bombo = [[equipo for equipo in equipos if equipo.bombo == i] for i in range(1,5)]  
    bombos = [Bombo(i+1, equipos_por_bombo[i]) for i in range(len(equipos_por_bombo))]
    grupos[0].nuevo_equipo(PAL)
    bombos[0].quitar_equipo(0)
    for bombo in bombos:
        bombo.sortear(grupos)
    AD = pd.DataFrame()
    EG = pd.DataFrame()
    for i, grupo in enumerate(grupos):
        nombres = [equipo.nombre for equipo in grupo.equipos]
        temp_df = pd.DataFrame(data = nombres, columns = [grupo.nombre])
        if i <= 3:
            AD = pd.concat([AD, temp_df], axis = 1)
        else:
            EG = pd.concat([EG, temp_df], axis = 1)
    tablas_grupos = [AD.to_html(classes = 'gruposA-D', index=False), EG.to_html(classes = 'gruposE-G', index=False)]
    return tablas_grupos
