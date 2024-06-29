import pygame as py  # Importa la biblioteca Pygame y la renombra como py
import sys  # Importa el módulo sys
import win32api, win32con, win32gui  # Importa módulos de Windows para manejar la ventana
from random import randint
from Mapa import Mapa  # Importa la función randint del módulo random

"""
La clase Window se encarga de manejar la ventana del juego, desde la creacion
de la ventana, el manejo de eventos, la actualizacion de la pantalla, la
posicion del jugador en la pantalla, la posicion relativa del jugador, la
preparacion de la pantalla para el inicio del juego y la actualizacion de la
pantalla
"""
class Window:
    """
    La funcion __init__() se encarga de inicializar las variables mas importantes
    dentro del programa, como el tamaño de la pantalla, el tamaño del mapa, el
    archivo en que se dirigira el nivel/mapa, el tipo de juego, que puede
    ser tanto un jugador como dos jugadores, y las variables r, g y b, que
    se encargan de que al jugar en 2 jugadores, la linea del centro vaya siempre
    variando en color
    """
    def __init__(self):
        py.init()
        self.screen = None
        self.screen_size = self.screen_width, self.screen_height = py.display.get_desktop_sizes()[0]
        self.map_size = self.map_width, self.map_height = 10000, 10000
        self.size_level = 100
        self.size_rect = max(self.map_size) / self.size_level
        self.matriz_nivel = []
        self.nomarch = r"Niveles\Niveles de prueba\level1_test.txt"
        self.tipo_juego = None
        self.r = randint(0, 255)
        self.g = randint(0, 255)
        self.b = randint(0, 255)
        self.mapa = None
    
    """
    la funcion crear_mapa() se encarga de crear un nuevo mapa, en base a los 
    parametros de __init__(), y si ya existe un mapa, se guarda el nivel actual,
    eso si estuviera implementado correctamente el guardar_nivel()
    """
    def crear_mapa(self, nomarch):
        if self.mapa != None:
            self.mapa.guardar_nivel()
        self.mapa = Mapa(self.map_size, self.size_rect, self.size_level, nomarch)
        self.mapa.start(self.tipo_juego)

    """
    La funcion move_window_to_center() se encarga de mover la ventana del juego
    al centro de la pantalla, como no me siento bien sin dar el credito, esta 
    funcion fue dada por ChatGPT en su totalidad (el chat se borro hace tiempo
    por diversas cuestiones, pero la funcion es de ChatGPT)
    """
    def move_window_to_center(self):
        hwnd = py.display.get_wm_info()["window"]
        monitor_info = win32api.GetMonitorInfo(win32api.MonitorFromPoint((0,0)))
        monitor_width = monitor_info.get("Monitor", (0, 0, 0, 0))[2]
        monitor_height = monitor_info.get("Monitor", (0, 0, 0, 0))[3]
        window_rect = win32gui.GetWindowRect(hwnd)
        window_width = window_rect[2] - window_rect[0]
        window_height = window_rect[3] - window_rect[1]
        x = int((monitor_width - window_width) / 2)
        y = int((monitor_height - window_height) / 2)
        win32gui.MoveWindow(hwnd, x, y, window_width, window_height, True)

    """
    La funcion handle_events() se encarga de manejar el cierre de la ventana del
    juego, lo que a su vez terminaria la ejecucion del programa
    """
    def handle_events(self):
        for event in py.event.get():
            if event.type == py.QUIT:
                py.quit()
                sys.exit()

    """
    la funcion handle_screen() se encarga de manejar la pantalla del juego, de 
    forma que posiciona el mapa en base a la posicion actual del jugador, y si
    el tipo de juego es de dos jugadores, se encarga de posicionar el mapa de
    forma que ambos jugadores puedan ver su parte del mapa, ademas de la linea
    divisoria que se encarga de separar a ambos jugadores
    """
    def handle_screen(self):
        self.screen.fill((0, 0, 0))
        self.screen_size = py.display.get_window_size()
        if self.tipo_juego == "un_jugador":
            self.screen.blit(self.mapa.nivel, self.pos)
        if self.tipo_juego == "dos_jugadores":
            self.r += randint(0, 1)
            self.g += randint(0, 1)
            self.b += randint(0, 1)
            if self.r >= 255:
                self.r -= 1
            if self.r <= 0:
                self.r += 1
            if self.g >= 255:
                self.g -= 1
            if self.g <= 0:
                self.g += 1
            if self.b >= 255:
                self.b -= 1
            if self.b <= 0:
                self.b += 1
            self.screen.blit(self.right_surf, self.right_pos)
            sobresaliente_izquierdo = self.map_width - self.screen_width - abs(self.left_pos[0])
            mitad_izquierda = py.Rect(0, 0, self.map_width - sobresaliente_izquierdo - self.screen_width//2 - self.size_rect//2, self.map_height)
            self.screen.blit(self.left_surf, self.left_pos, area=mitad_izquierda)
            separacion = py.Surface((self.size_rect//2, self.screen_height))
            separacion.fill((self.r, self.g, self.b))
            self.screen.blit(separacion, (self.screen_width//2 - self.size_rect//2, 0))

    """
    la funcion set_map() se encarga de posicionar el mapa en base al tipo de juego
    """
    def set_map(self):
        if self.tipo_juego == "un_jugador":
            self.pos = [(self.screen_width - self.map_width)//2 - self.size_rect, (self.screen_height - self.map_height)//2 - self.size_rect]
            self.nivel = self.mapa.nivel
        if self.tipo_juego == "dos_jugadores":
            self.left_pos = [(self.screen_width - self.map_width)//4 - self.size_rect, (self.screen_height - self.map_height)//2 - self.size_rect]
            self.left_surf = self.mapa.left_surf
            self.right_pos = [(self.screen_width - self.map_width) + self.map_width//4 - self.size_rect*5, (self.screen_height - self.map_height)//2 - self.size_rect]
            self.right_surf = self.mapa.right_surf
    """
    La funcion player_pos_screen() se encarga de posicionar al jugador en la pantalla
    dependiendo de que tipo de juego se seleccione
    """
    def player_pos_screen(self, jugador = "Jugador 1"):
        if self.tipo_juego == "un_jugador":
            return [n//2 - self.size_rect//2  for n in self.screen_size]
        if self.tipo_juego == "dos_jugadores":
            if jugador == "Jugador 1":
                return [self.screen_size[0]//4 - self.size_rect, self.screen_size[1]//2 - self.size_rect]
            if jugador == "Jugador 2":
                return [self.screen_size[0] - self.screen_size[0]//4 - self.size_rect * 1.15, self.screen_size[1]//2 - self.size_rect]

    """
    la funcion player_relative_pos_screen() se encarga de retornar la posicion
    relativa del jugador, la cual se maneja con una matriz que internamente sigue
    al jugador en el mapa
    """
    def player_relative_pos_screen(self, jugador = "Jugador 1"):
        if self.tipo_juego == "un_jugador":
            return [len(self.matriz_nivel)/2] * 2
        if self.tipo_juego == "dos_jugadores":
            if jugador == "Jugador 1":
                return [len(self.matriz_nivel)/4, len(self.matriz_nivel)/2]
            if jugador == "Jugador 2":
                return [len(self.matriz_nivel)*0.75, len(self.matriz_nivel)/2]

    """
    La funcion pre_start() se encarga de preparar la pantalla para el inicio del
    juego, en base al tipo de juego que se seleccione, se crea el mapa, se posiciona
    el mapa y se setea el mapa
    """
    def pre_start(self, tipo_juego="un_jugador"):
        self.tipo_juego = tipo_juego
        self.crear_mapa(self.nomarch)
        self.set_map()

    """
    La funcion start() crea la ventana del juego y la centra
    """
    def start(self):
        self.screen = py.display.set_mode([n - 100 for n in list(self.screen_size)], py.RESIZABLE)
        self.move_window_to_center()

    """
    La funcion update() se encarga de actualizar la pantalla del juego
    """
    def update(self):
        self.handle_events()
        self.handle_screen()

"""
Inicia el programa
"""
if  __name__ == "__main__":
    exec(open("Juego.py").read())
        