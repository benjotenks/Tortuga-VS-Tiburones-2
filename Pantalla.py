import pygame as py  # Importa la biblioteca Pygame y la renombra como py
import sys  # Importa el módulo sys
import win32api, win32con, win32gui  # Importa módulos de Windows para manejar la ventana
from random import randint
from Mapa import Mapa  # Importa la función randint del módulo random

class Window:
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

    def crear_mapa(self, nomarch):
        if self.mapa != None:
            self.mapa.guardar_nivel()
        self.mapa = Mapa(self.map_size, self.size_rect, self.size_level, nomarch)
        self.mapa.start(self.tipo_juego)

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

    def handle_events(self):
        for event in py.event.get():
            if event.type == py.QUIT:
                py.quit()
                sys.exit()

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
        #print(f"self.pos: {self.pos}")

    def set_map(self):
        if self.tipo_juego == "un_jugador":
            self.pos = [(self.screen_width - self.map_width)//2 - self.size_rect, (self.screen_height - self.map_height)//2 - self.size_rect]
            self.nivel = self.mapa.nivel
        if self.tipo_juego == "dos_jugadores":
            self.left_pos = [(self.screen_width - self.map_width)//4 - self.size_rect, (self.screen_height - self.map_height)//2 - self.size_rect]
            self.left_surf = self.mapa.left_surf
            self.right_pos = [(self.screen_width - self.map_width) + self.map_width//4 - self.size_rect*5, (self.screen_height - self.map_height)//2 - self.size_rect]
            self.right_surf = self.mapa.right_surf

    def player_pos_screen(self, jugador = "Jugador 1"):
        if self.tipo_juego == "un_jugador":
            return [n//2 - self.size_rect//2  for n in self.screen_size]
        if self.tipo_juego == "dos_jugadores":
            if jugador == "Jugador 1":
                return [self.screen_size[0]//4 - self.size_rect, self.screen_size[1]//2 - self.size_rect]
            if jugador == "Jugador 2":
                return [self.screen_size[0] - self.screen_size[0]//4 - self.size_rect * 1.15, self.screen_size[1]//2 - self.size_rect]
            
    def player_relative_pos_screen(self, jugador = "Jugador 1"):
        if self.tipo_juego == "un_jugador":
            return [len(self.matriz_nivel)/2] * 2
        if self.tipo_juego == "dos_jugadores":
            if jugador == "Jugador 1":
                return [len(self.matriz_nivel)/4, len(self.matriz_nivel)/2]
            if jugador == "Jugador 2":
                return [len(self.matriz_nivel)*0.75, len(self.matriz_nivel)/2]
            
    def pre_start(self, tipo_juego="un_jugador"):
        self.tipo_juego = tipo_juego
        self.crear_mapa(self.nomarch)
        self.set_map()

    def start(self):
        self.screen = py.display.set_mode([n - 100 for n in list(self.screen_size)], py.RESIZABLE)
        self.move_window_to_center()

    def update(self):
        self.handle_events()
        self.handle_screen()

if  __name__ == "__main__":
    exec(open("Juego.py").read())
        