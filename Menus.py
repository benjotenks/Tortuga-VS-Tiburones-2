import pygame as py  # Importa la biblioteca Pygame y la renombra como py
from Personajes import Tortuga  # Importa la clase Player desde el módulo Personajes
import sys  # Importa el módulo sys

COLORS = {  # Define un diccionario con colores
    "white" : ( 255, 255, 255),  # Color blanco
    "black" : (   0,   0,   0),  # Color negro
    "red"   : ( 255,   0,   0),  # Color rojo
    "blue"  : (   0,   0, 255)   # Color azul
}

class Menu:  # Define la clase Menu
    def __init__(self):  # Constructor de la clase Menu
        py.init()  # Inicializa Pygame
        py.display.set_caption("MENU Tortugas vs Tiburones")  # Establece el título de la ventana
        self.screen_size = self.screen_width, self.screen_height = 800, 500  # Tamaño de la ventana
        self.button_size = self.button_width, self.button_height = 400, 100  # Tamaño de los botones
        self.image_size = self.image_width, self.image_height = 150, 150  # Tamaño de las imágenes
        self.fuente = py.font.Font(None, 36)  # Carga una fuente
        self.screen = py.display.set_mode(self.screen_size)  # Crea la ventana
        self.click = False  # Variable para detectar clics del mouse
        self.posibles_tipos = []  # Lista para almacenar los tipos de jugadores posibles
        self.jugador = "Jugador 1"  # Define el jugador por defecto como "Jugador 1"
        
    def start(self):  # Método para iniciar el menú
        return self.menu_principal()  # Llama al método del menú principal

    def salir(self):  # Método para salir del juego
        self.cierre_ventana()  # Llama al método para cerrar la ventana
      
    def cierre_ventana(self):  # Método para cerrar la ventana del juego
        py.quit()  # Sale de Pygame
        sys.exit()  # Sale del programa
        
    def handle_events(self):  # Método para manejar eventos
        for event in py.event.get():  # Itera sobre los eventos
            if event.type == py.QUIT:  # Si se presiona el botón de cerrar la ventana
                self.cierre_ventana()  # Llama al método para cerrar la ventana
            if event.type == py.MOUSEBUTTONDOWN:  # Si se presiona un botón del mouse
                self.click = True  # Marca que se ha hecho clic
                
    def crear_botones(self, opciones, tipo_menu = "None"):  # Método para crear botones
        lista = []  # Lista para almacenar los botones
        for key in opciones:  # Itera sobre las opciones
            temp = []  # Lista temporal para almacenar los datos del botón
            if tipo_menu == "None":  # Si no se especifica un tipo de menú
                # Crea un botón con el texto correspondiente
                boton = py.Rect(opciones[key][0], opciones[key][1], opciones[key][2], opciones[key][3])
                boton_surf = self.fuente.render(key, True, COLORS["white"])  # Renderiza el texto del botón
                boton_rect = boton_surf.get_rect(center = boton.center)  # Obtiene el rectángulo del botón
                temp.append(boton)  # Agrega el botón a la lista temporal
                temp.append(boton_surf)  # Agrega el texto del botón a la lista temporal
                temp.append(boton_rect)  # Agrega el rectángulo del botón a la lista temporal
            if tipo_menu == "Character_select":  # Si se especifica un tipo de menú de selección de personajes
                if key != "Imagen" + " " + f"{self.posibles_tipos[self.index_posibles_tipos]}":
                    # Crea un botón con el texto correspondiente
                    boton = py.Rect(opciones[key][0], opciones[key][1], opciones[key][2], opciones[key][3])
                    boton_surf = self.fuente.render(key, True, COLORS["white"])  # Renderiza el texto del botón
                    boton_rect = boton_surf.get_rect(center = boton.center)  # Obtiene el rectángulo del botón
                    temp.append(boton)  # Agrega el botón a la lista temporal
                    temp.append(boton_surf)  # Agrega el texto del botón a la lista temporal
                    temp.append(boton_rect)  # Agrega el rectángulo del botón a la lista temporal
                else:
                    # Carga la imagen del jugador y renderiza su nombre
                    imagen = py.image.load(self.directorio_imagen)
                    imagen = py.transform.scale(imagen, self.image_size)
                    texto = self.fuente.render(self.jugador, True, COLORS["white"])
                    self.image_size = self.image_width, self.image_height = imagen.get_rect().size
                    self.size_text = self.text_width, self.text_height = texto.get_rect().size
                    self.posicion_imagen = ((self.screen_width - self.image_width)//2, (self.screen_height - self.image_height)//8)
                    self.posicion_texto = ((self.screen_width - self.text_width)//2, (self.posicion_imagen[1] - self.text_height))
                    temp.append(imagen)  # Agrega la imagen a la lista temporal
                    temp.append(texto)  # Agrega el texto a la lista temporal
            lista.append(temp)  # Agrega la lista temporal a la lista de botones
        return lista  # Retorna la lista de botones
    
    def menu_principal(self):  # Método para el menú principal
        self.click = False  # Restablece la variable de clic
        opciones = {  # Opciones del menú principal
            "Un Jugador"   : (self.screen_width//2 - self.button_width//2, self.screen_height//8 - self.button_height//8, self.button_width, self.button_height),
            "Multijugador" : (self.screen_width//2 - self.button_width//2, self.screen_height//2 - self.button_height//2, self.button_width, self.button_height), 
            "Salir"        : (self.screen_width//2 - self.button_width//2, self.screen_height//2 + self.button_height, self.button_width, self.button_height)
        }
        botones = self.crear_botones(opciones)  # Crea los botones del menú principal

        running = True  # Bandera para controlar el bucle principal
        while running:  # Bucle principal del menú principal
            self.screen.fill(COLORS["black"])  # Rellena la pantalla con color negro
            self.handle_events()  # Maneja los eventos del juego
            mouse_pos = py.mouse.get_pos()  # Obtiene la posición del mouse
            for i in range(len(botones)):  # Itera sobre los botones
                if botones[i][0].collidepoint(mouse_pos):  # Si el mouse está sobre el botón
                    py.draw.rect(self.screen, COLORS["blue"], botones[i][0])  # Dibuja el botón en azul
                    if self.click:  # Si se hace clic en el botón
                        if i == 0:  # Si se hace clic en "Un Jugador"
                            temp = self.un_jugador()  # Llama al método para el menú de un jugador
                            if temp != None:  # Si se selecciona una opción válida
                                return temp  # Retorna la opción seleccionada
                        if i == 1:  # Si se hace clic en "Multijugador"
                            temp = self.multijugador()  # Llama al método para el menú de multijugador
                            if temp != None:  # Si se selecciona una opción válida
                                return temp  # Retorna la opción seleccionada
                        if i == 2:  # Si se hace clic en "Salir"
                            self.salir()  # Llama al método para salir del juego
                        self.screen.fill(COLORS["black"])  # Rellena la pantalla con color negro
                        break  # Sale del bucle
                else:  # Si el mouse no está sobre el botón
                    py.draw.rect(self.screen, COLORS["red"], botones[i][0])  # Dibuja el botón en rojo
                if running:  # Si el juego está en ejecución
                    self.screen.blit(botones[i][1], botones[i][2])  # Dibuja el texto del botón en la pantalla

            self.click = False  # Restablece la variable de clic
            py.display.flip()  # Actualiza la pantalla

    # Los métodos siguientes tienen una estructura similar al método menu_principal y realizan funciones similares, así que no es necesario comentarlos línea por línea
    # Se maneja el menú de un jugador, el menú de multijugador y la selección de personajes, mostrando botones y permitiendo al jugador interactuar con ellos


    def un_jugador(self):
        self.click = False
        opciones = {"Comenzar"   : (self.screen_width//2 - self.button_width//2, self.screen_height//8 - self.button_height//8, self.button_width, self.button_height),
                    "Volver"     : (self.screen_width//2 - self.button_width//2, self.screen_height//2 - self.button_height//2, self.button_width, self.button_height),
                    "Salir"      : (self.screen_width//2 - self.button_width//2, self.screen_height//2 + self.button_height, self.button_width, self.button_height)
                    }
        botones = self.crear_botones(opciones)
        running = True
        while running:
            self.screen.fill(COLORS["black"])
            self.handle_events()
            mouse_pos = py.mouse.get_pos()

            for i in range(len(botones)):
                if botones[i][0].collidepoint(mouse_pos):
                    py.draw.rect(self.screen, COLORS["blue"], botones[i][0])
                    if self.click:
                        if i == 0:
                            temp = self.un_jugador.__name__
                            if temp != None:
                                return  temp
                        if i == 1:
                            return None
                        if i == 2:
                            self.salir()
                        self.screen.fill(COLORS["black"])
                        break
                else:
                    py.draw.rect(self.screen, COLORS["red"], botones[i][0])
                if running:
                    self.screen.blit(botones[i][1], botones[i][2])

            self.click = False
            py.display.flip()
            
    def multijugador(self):
        self.click = False
        opciones = {f"Dos Jugadores"     : ((0), (self.screen_height - self.button_height)//2, self.button_width, self.button_height), 
                    "Dos Jugadores Lan"  : ((self.screen_width- self.button_width), (self.screen_height - self.button_height)//2, self.button_width, self.button_height),
                    "Volver"             : ((0), (self.screen_height - self.button_height), self.button_width, self.button_height),
                    "Salir"              : ((self.screen_width - self.button_width), (self.screen_height - self.button_height), self.button_width, self.button_height)
                    }
        botones = self.crear_botones(opciones)
        running = True
        while running:
            self.screen.fill(COLORS["black"])
            self.handle_events()
            mouse_pos = py.mouse.get_pos()
            for i in range(len(botones)):
                if botones[i][0].collidepoint(mouse_pos):
                    py.draw.rect(self.screen, COLORS["blue"], botones[i][0])
                    if self.click:
                        if i == 0:
                            temp = self.dos_jugadores()
                            if temp != None:
                                return temp
                        if i == 1:
                            temp = self.dos_jugadores_lan()
                            if temp != None:
                                return temp
                        if i == 2:
                            return None
                        if i == 3:
                            self.salir()
                        self.screen.fill(COLORS["black"])
                        break
                else:
                    py.draw.rect(self.screen, COLORS["red"], botones[i][0])
                if running:
                    self.screen.blit(botones[i][1], botones[i][2])

            self.click = False
            py.display.flip()
            
    def dos_jugadores(self):
        return self.dos_jugadores.__name__       

    def dos_jugadores_lan(self):
        return self.dos_jugadores_lan.__name__

    def player_select(self, jugador):
        self.click = False
        self.jugador = jugador
        self.posibles_tipos = Tortuga()
        directorio = self.posibles_tipos.directorio
        self.posibles_tipos = self.posibles_tipos.posibles_tipos
        self.index_posibles_tipos = 0
        posibles_tipos = {}
        with open(directorio, "r") as arch:
            for index, linea in enumerate(arch):
                if index != 0:
                    linea = linea.strip()
                    linea = linea.split(";")
                    for j in self.posibles_tipos:
                        if linea[0].split()[0] == "Tortuga" and linea[0] not in posibles_tipos:
                            posibles_tipos[linea[0]] = linea[5]
        running = True
        while running:
            self.screen.fill(COLORS["black"]) #
            opciones = {"Imagen" + " " + f"{self.posibles_tipos[self.index_posibles_tipos]}"   : (self.screen_width//2 - self.button_width//2, self.screen_height//8 - self.button_height//8, self.image_width, self.image_height),
                        f"{self.posibles_tipos[self.index_posibles_tipos]}" : ((0), (self.screen_height - self.button_height)//2, self.button_width, self.button_height), 
                        "Listo"  : ((self.screen_width- self.button_width), (self.screen_height - self.button_height)//2, self.button_width, self.button_height),
                        "No hago nada" : ((0), (self.screen_height - self.button_height), self.button_width, self.button_height),
                        "Salir"  : ((self.screen_width - self.button_width), (self.screen_height - self.button_height), self.button_width, self.button_height)
                        }
            self.tipo = self.posibles_tipos[self.index_posibles_tipos]
            self.directorio_imagen = posibles_tipos[self.tipo]
            botones = self.crear_botones(opciones, "Character_select")
            self.handle_events()
            mouse_pos = py.mouse.get_pos()
            for i in range(len(botones)):
                if i != 0:
                    if botones[i][0].collidepoint(mouse_pos):
                        py.draw.rect(self.screen, COLORS["blue"], botones[i][0])
                        if self.click:
                            if i == 1:
                                if self.index_posibles_tipos == len(self.posibles_tipos) - 1:
                                    self.index_posibles_tipos = 0
                                else:
                                    self.index_posibles_tipos += 1
                            if i == 2:
                                return Tortuga(self.tipo, jugador)
                            if i == 3:
                                pass
                            if i == 4:
                                self.salir()
                            self.screen.fill(COLORS["black"])
                            break
                    else:
                        py.draw.rect(self.screen, COLORS["red"], botones[i][0])
                    if running:
                        self.screen.blit(botones[i][1], botones[i][2])
                else:
                    self.screen.blit(botones[i][0], self.posicion_imagen) #(opciones["Imagen" + " " + f"{self.posibles_tipos[self.index_posibles_tipos]}"][2], opciones["Imagen" + " " + f"{self.posibles_tipos[self.index_posibles_tipos]}"][3])
                    if running:
                        self.screen.blit(botones[i][1], self.posicion_texto)
                    
                    pass
            self.click = False
            py.display.flip()
                
if  __name__ == "__main__":
    exec(open("Juego.py").read())
        