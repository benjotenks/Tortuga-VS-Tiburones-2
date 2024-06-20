import pygame as py
from random import randint

# Define colores
COLORS = {
    "#6C3483" : (108, 52, 131),
    "#2874A6" : (40, 116, 166 ),
    "#117A65"   : (17, 122, 101),
    "#239B56"  : (35, 155, 86 )
}

class Mapa:
    def __init__(self, map_size, size_rect, size_level, nomarch):
        self.map_size = map_size
        self.size_rect = size_rect
        self.size_level = size_level
        self.nomarch = nomarch
        self.matriz_nivel = []
        self.nivel = []
        self.tipo_juego = None
        self.left_surf = None
        self.right_surf = None
        self.tipo_juego = None

    def generar_prueba(self):
        with open(self.nomarch, "w") as arch:
            for _ in range(self.size_level):
                for _ in range(self.size_level):
                    valor_aleatorio = randint(0, len(COLORS) - 1)
                    arch.write(f"{valor_aleatorio}" + " ")
                arch.write("\n")
                
    def lectura_nivel_archivo(self):
        with open(self.nomarch, "r") as arch:
            for linea in arch:
                linea = linea.strip()
                fila = linea.split(" ")
                self.matriz_nivel.append(fila)    

    def crear_nivel(self):
        self.nivel = py.Surface(self.map_size)
        colores = [key for key in COLORS]
        if self.tipo_juego == "un_jugador":
            for index_fila in range(len(self.matriz_nivel)):
                for index_columna, valor in enumerate(self.matriz_nivel[index_fila]):
                    valor = int(valor)
                    color = colores[valor]
                    py.draw.rect(self.nivel, COLORS[color], (index_columna * self.size_rect, index_fila * self.size_rect, self.size_rect, self.size_rect))
        if self.tipo_juego == "dos_jugadores":
            self.left_surf = py.Surface(self.map_size)
            self.right_surf = py.Surface(self.map_size)
            colores = [key for key in COLORS]
            for index_fila in range(len(self.matriz_nivel)):
                for index_columna, valor in enumerate(self.matriz_nivel[index_fila]):
                    valor = int(valor)
                    color = colores[valor]
                    py.draw.rect(self.left_surf, COLORS[color], (index_columna * self.size_rect, index_fila * self.size_rect, self.size_rect, self.size_rect))
                    py.draw.rect(self.right_surf, COLORS[color], (index_columna * self.size_rect, index_fila * self.size_rect, self.size_rect, self.size_rect))   
    
    def guardar_nivel(self):
        pass
    
    def start(self, tipo_juego):
        self.tipo_juego = tipo_juego
        self.generar_prueba()
        self.lectura_nivel_archivo()
        self.crear_nivel()


