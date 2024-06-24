from Personajes import Tortuga as Jugador  # Importa la clase Player desde el módulo Personajes y la renombra como Jugador
from Personajes import Tiburon as Enemigo
from Personajes import pantalla  # Importa la variable pantalla desde el módulo Personajes
from Menus import Menu  # Importa la clase Menu desde el módulo Menus
import pygame as py  # Importa la biblioteca Pygame y la renombra como py
from random import randrange
import socket, threading, sys  # Importa los módulos socket, threading y sys



class Game:
    def __init__(self):
        py.init()  # Inicializa Pygame
        self.tipo_juego = "un_jugador"  # Configura el tipo de juego como "un_jugador" por defecto
        self.enemigos = []
        self.generacion_alternante = "un_jugador"
        
    def start(self):
        self.menu = Menu()  # Crea una instancia de la clase Menu
        self.tipo_juego = self.menu.start()  # El usuario selecciona el tipo de juego
        self.comenzar()  # Inicia el juego
    
    def crear_enemigo(self):
        if self.tipo_juego == "un_jugador":
            enemigo = Enemigo("Tiburon Espada")
            enemigo.character_pos_screen()
            self.enemigos.append(enemigo)
        if self.tipo_juego == "dos_jugadores":
            enemigoa = Enemigo("Tiburon Espada")
            enemigob = Enemigo("Tiburon Espada")
            enemigoa.character_pos_screen()
            enemigob.character_pos_screen()
            self.enemigos.append(enemigoa)
            self.enemigos.append(enemigob)
    
    def update(self):
        pantalla.update()  # Actualiza la pantalla
        if self.tipo_juego == "un_jugador":
            self.jugador_1.update(self.tipo_juego)  # Actualiza el jugador 1 en el juego de un jugador
        if self.tipo_juego == "dos_jugadores":
            self.jugador_1.update(self.tipo_juego)  # Actualiza el jugador 1 en el juego de dos jugadores
            self.jugador_2.update(self.tipo_juego)  # Actualiza el jugador 2 en el juego de dos jugadores
        if len(self.enemigos) <= (10 if self.tipo_juego == "un_jugador" else 20):
            self.crear_enemigo()
        for enemigo in self.enemigos:
            enemigo.update(self.tipo_juego, "Jugador 1")
            #enemigo.update()
        
    def comenzar(self):
        FPS = 60  # Velocidad de fotogramas por segundo
        clock = py.time.Clock()  # Crea un objeto Clock para controlar la velocidad de fotogramas
        pantalla.pre_start(self.tipo_juego)  # Prepara la pantalla para el inicio del juego
        if self.tipo_juego == "un_jugador":
            self.jugador_1 = self.menu.player_select("Jugador 1")  # El jugador 1 selecciona su personaje
            self.jugador_1.character_pos_screen()  # Posiciona al jugador 1 en la pantalla
        if self.tipo_juego == "dos_jugadores":
            self.jugador_1 = self.menu.player_select("Jugador 1")  # El jugador 1 selecciona su personaje
            self.jugador_2 = self.menu.player_select("Jugador 2")  # El jugador 2 selecciona su personaje
            self.jugador_1.character_pos_screen()  # Posiciona al jugador 1 en la pantalla
            self.jugador_2.character_pos_screen()  # Posiciona al jugador 2 en la pantalla
            
        if self.tipo_juego == "un_jugador" or self.tipo_juego == "dos_jugadores":
            pantalla.start()  # Inicia la pantalla
            
        while True:  # Bucle principal del juego
            self.update()  # Actualiza el juego en cada iteración
            py.display.flip()  # Actualiza la pantalla
            clock.tick(FPS)  # Controla la velocidad de fotogramas

if  __name__ == "__main__":
    juego = Game()  # Crea una instancia de la clase Game
    juego.start()  # Inicia el juego