import pygame as py
from random import randrange
from math import degrees, atan2, tan, cos, sin, sqrt, radians
from Pantalla import Window as window

py.init()
pantalla = window()
class Character:
    def __init__(self, tipo = "None"):
        self.atacando = False
        self.pos = [0, 0]
        self.relative_pos = [0, 0]
        self.health = 0
        self.damage = 0
        self.movement = 0
        self.tipo = tipo
        self.special_atack = "None"
        self.imagen = None
        self.rect = None
        self.factor_velocidad = 10 #Creo que es estupidamente importante
        self.mov_w = 0
        self.mov_s = 0
        self.mov_a = 0
        self.mov_d = 0
        self.directorio = r"personajes.csv"
        self.posibles_tipos = []
        self.num_angles = 360
        self.imagen_prerotada = []
        self.angulo_necesario = (75 if self.__class__.__name__ == "Tortuga" else 345) # En caso de problemas de rotacion revisar este valor
        with open(self.directorio, "r") as arch:
            for index, linea in enumerate(arch):
                if index != 0:
                    linea = linea.strip()
                    linea = linea.split(";")
                    if linea[0].split()[0] == self.__class__.__name__ and linea[0] not in self.posibles_tipos:
                        self.posibles_tipos.append(linea[0])
        self.definir_estadisticas()
    
    def definir_estadisticas(self):
        with open(self.directorio, "r") as arch:
            for index, linea in enumerate(arch):
                if not index == 0:
                    linea = linea.strip()
                    linea = linea.split(";")
                    tipo_en_csv = linea[0]
                    if tipo_en_csv == self.tipo:
                        self.velocidad = float(linea[3])
                        self.health = float(linea[1])
                        self.damage = float(linea[2])
                        self.movement = (self.velocidad * pantalla.size_rect)/self.factor_velocidad
                        self.special_atack = linea[4]
                        self.imagen = py.image.load(linea[5])
                        self.imagen = py.transform.scale(self.imagen, (float(linea[6]) * pantalla.size_rect, float(linea[7]) * pantalla.size_rect))
                        self.imagen_prerotada = [py.transform.rotate(self.imagen, angle) for angle in range(self.num_angles)]
                        
    def character_pos_screen(self):
        if self.__class__.__name__ == "Tortuga":
            self.pos = pantalla.player_pos_screen(self.jugador)
            self.relative_pos = pantalla.player_relative_pos_screen(self.jugador)
        if self.__class__.__name__ == "Tiburon":
            self.pos = [randrange(-pantalla.map_width, pantalla.map_width, 100), 0] # [0, 100]#
            
        self.rect = self.imagen.get_rect(center = self.pos)
        self.rect.inflate_ip(-pantalla.size_rect//2, -pantalla.size_rect//2)
        self.hitbox = py.Rect(0, 0, pantalla.size_rect//2, pantalla.size_rect//2)
        self.hitbox.center = self.rect.bottomright
        
        self.circle_center = [n + pantalla.size_rect//4 for n in self.pos]
        if self.__class__.__name__ == "Tiburon":
            self.circle_center = [n + pantalla.size_rect//4 for n in self.circle_center]
        self.circle_radius = pantalla.size_rect//2
        
        self.hitbox_ataque = py.Rect(0, 0, pantalla.size_rect//4, pantalla.size_rect//4)
        self.hitbox_ataque.center = self.circle_center

        initial_mouse_x, initial_mouse_y = py.mouse.get_pos()
        # dx = initial_mouse_x - self.rect.centerx
        # dy = initial_mouse_y - self.rect.centery
        # # initial_angle = degrees(atan2(-dy, dx))
        # # initial_angle_index = int((initial_angle - self.angulo_necesario) * self.num_angles / 360)
        self.imagen = self.imagen_prerotada[0]
                                          
    def start_relative_pos(self):
        pass

    def ajustar_atributo(self, **atributos):
        for key in atributos:
            if key == "health":
                self.health += atributos[key]
            if key == "damage":
                self.damage += atributos[key]
            if key == "movemente":
                self.movement += atributos[key]
    
    def __str__(self):
        print(f"health: {self.health}" + "\n" +
              f"damage: {self.damage}" + "\n" +
              f"movement: {self.movement}" + "\n" +
              f"special_atack: {self.special_atack}" + "\n"
              f"tipo: {self.tipo}" + "\n"
              )
        return ""
    
class Tortuga(Character):
    def __init__(self, tipo = "None", jugador = "Jugador 1"):
        super().__init__(tipo)
        self.jugador = jugador
    
    def rotar(self):
        mouse_pos = py.mouse.get_pos()
        dx = mouse_pos[0] - self.rect.centerx
        dy = mouse_pos[1] - self.rect.centery
        angle = degrees(atan2(-dy, dx))
        angle_index = int((angle - self.angulo_necesario) * self.num_angles / 360) 
        self.imagen = self.imagen_prerotada[angle_index]
        self.rect = self.imagen.get_rect(center = self.rect.center)
        self.rect.inflate_ip(-pantalla.size_rect//2, -pantalla.size_rect//2)
        # Obtener la posición del mouse
        mouse_x, mouse_y = py.mouse.get_pos()

        # Calcular la distancia entre el centro del círculo y la posición del mouse
        distance = sqrt((mouse_x - self.circle_center[0]) ** 2 + (mouse_y - self.circle_center[1]) ** 2)

        # Limitar la posición del rectángulo para que permanezca dentro del círculo
        if distance <= self.circle_radius:
            self.hitbox_ataque.center = (mouse_x, mouse_y)
        else:
            # Si el mouse está fuera del círculo, calcular la posición dentro del círculo
            angle = atan2(mouse_y - self.circle_center[1], mouse_x - self.circle_center[0])
            self.hitbox_ataque.center = (
                int(self.circle_center[0] + self.circle_radius * cos(angle)),
                int(self.circle_center[1] + self.circle_radius * sin(angle))
            )

    def mover(self, tipo_juego):
        keys = py.key.get_pressed()
        if tipo_juego == "un_jugador":
            if keys[py.K_w] or keys[py.K_UP]: #Moviiento hacia arriba
                if pantalla.pos[1] <= 0: #Limite superior antes de salir del mapa
                    pantalla.pos[1] += self.movement
                    if self.mov_w >= self.factor_velocidad - 1:
                        self.relative_pos[1] += self.velocidad
                        self.mov_w = 0
                    else:
                        self.mov_w += 1
            if keys[py.K_s] or keys[py.K_DOWN]: #Movimiento hacia abajo
                if pantalla.pos[1] >= -pantalla.map_height + pantalla.screen_height:
                    pantalla.pos[1] -= self.movement
                    if self.mov_s >= self.factor_velocidad - 1:
                        self.relative_pos[1] -= self.velocidad
                        self.mov_s = 0
                    else:
                        self.mov_s += 1
            if keys[py.K_a] or keys[py.K_LEFT]: #Movimiento a la izquierda
                if pantalla.pos[0] <= 0:
                    pantalla.pos[0] += self.movement
                    if self.mov_a == self.factor_velocidad - 1:
                        self.relative_pos[0] -= self.velocidad
                        self.mov_a = 0
                    else:
                        self.mov_a += 1
            if keys[py.K_d] or keys[py.K_RIGHT]: #Movimiento a la derecha
                if pantalla.pos[0] >= -pantalla.map_width + pantalla.screen_width:
                    pantalla.pos[0] -= self.movement
                    if self.mov_d == self.factor_velocidad - 1:
                        self.relative_pos[0] += self.velocidad
                        self.mov_d = 0
                    else:
                        self.mov_d += 1
        if tipo_juego == "dos_jugadores":
            if (keys[py.K_w] if self.jugador == "Jugador 1" else keys[py.K_UP]): #Moviiento hacia arriba
                if self.jugador == "Jugador 1":
                    pantalla.left_pos[1] += self.movement
                if self.jugador == "Jugador 2":
                    pantalla.right_pos[1] += self.movement
                if self.mov_w >= self.factor_velocidad - 1:
                    self.relative_pos[1] += self.velocidad
                    self.mov_w = 0
                else:
                    self.mov_w += 1
            if (keys[py.K_s] if self.jugador == "Jugador 1" else keys[py.K_DOWN]): #Movimiento hacia abajo
                if self.jugador == "Jugador 1":
                    pantalla.left_pos[1] -= self.movement
                if self.jugador == "Jugador 2":
                    pantalla.right_pos[1] -= self.movement
                if self.mov_s >= self.factor_velocidad - 1:
                    self.relative_pos[1] -= self.velocidad
                    self.mov_s = 0
                else:
                    self.mov_s += 1
            if (keys[py.K_a] if self.jugador == "Jugador 1" else keys[py.K_LEFT]): #Movimiento a la izquierda
                if self.jugador == "Jugador 1":
                    pantalla.left_pos[0] += self.movement
                if self.jugador == "Jugador 2":
                    pantalla.right_pos[0] += self.movement
                if self.mov_a == self.factor_velocidad - 1:
                    self.relative_pos[0] -= self.velocidad
                    self.mov_a = 0
                else:
                    self.mov_a += 1
            if (keys[py.K_d] if self.jugador == "Jugador 1" else keys[py.K_RIGHT]): #Movimiento a la derecha
                if self.jugador == "Jugador 1":
                    pantalla.left_pos[0] -= self.movement
                if self.jugador == "Jugador 2":
                    pantalla.right_pos[0] -= self.movement
                if self.mov_d == self.factor_velocidad - 1:
                    self.relative_pos[0] += self.velocidad
                    self.mov_d = 0
                else:
                    self.mov_d += 1    
        if py.mouse.get_pressed()[0]:
            self.atacando = True
        if not py.mouse.get_pressed()[0]:
            self.atacando = True
        #print(f"Jugador_ {self.jugador} | self.relative_pos: {self.relative_pos}") # Corregir posicionamiento de jugador 2, aparece 4 recuadros mas a la izquierda de lo que deberia
       
    def update(self, tipo_juego):
        pantalla.screen.blit(self.imagen, self.rect)
        self.mover(tipo_juego)
        self.rotar()

        # Hitboxes
        py.draw.circle(pantalla.screen, (0, 0, 0), self.circle_center, self.circle_radius, 2)
        py.draw.rect(pantalla.screen, (255, 0, 0), self.hitbox)
        py.draw.rect(pantalla.screen, (255, 0, 0), self.hitbox_ataque)
            
class Tiburon(Character):
    def __init__(self, tipo = "None"):
        super().__init__(tipo)
        
        self.start = True
        self.angle_movement = 0
    
    def mover(self):
        mov = [0, 0]
        
        # Calculate the direction towards the center of the screen
        center_x = pantalla.screen_width // 2
        center_y = pantalla.screen_height // 2
        dx = center_x - self.pos[0]
        dy = center_y - self.pos[1]
        
        # Normalize the direction vector
        magnitude = sqrt(dx ** 2 + dy ** 2)
        if magnitude != 0:
            dx /= magnitude
            dy /= magnitude

        # Encragado de buscar el centro de la pantalla ajustado al jugador
        dx -= pantalla.size_rect//2 / magnitude
        dy -= pantalla.size_rect//2 / magnitude
        
        # dispone el movimiento hacia el centro de la pantalla
        speed = self.movement  
        mov[0] = dx * speed
        mov[1] = dy * speed

        self.circle_center = [self.circle_center[_] + mov[_] for _ in range(2)]
        self.hitbox.center = self.circle_center
        self.hitbox_ataque.center = self.circle_center

        self.angle_movement = (0 if self.angle_movement >= 359 else 359 if self.angle_movement < 0 else self.angle_movement)
        self.pos = [self.pos[_] + mov[_] for _ in range(2)]
    
    def rotar(self):
        self.rect = self.imagen.get_rect(center = self.rect.bottomright)
        
        center_x = pantalla.screen_width // 2
        center_y = pantalla.screen_height // 2
        dx = center_x - self.pos[0]
        dy = center_y - self.pos[1]
        
        angle_needed = int(degrees(atan2(-dy, dx)))
        angle_needed = (angle_needed + 360) % 360  
        
        self.imagen = self.imagen_prerotada[angle_needed - 90]

    def update(self, tipo_juego = "un_jugador", jugador = "Jugador 1"):
        if tipo_juego == "un_jugador":
            if not self.start:
                diferencia = [n - pantalla.pos[i] for i, n in enumerate(self.temp)]
                self.temp = [n for n in pantalla.pos]   # No tocar
                self.pos[0] -= diferencia[0]
                self.pos[1] -= diferencia[1]
                self.circle_center = [self.circle_center[_] - diferencia[_] for _ in range(2)]
                self.hitbox.center = self.circle_center
                
                self.mover()
                self.rotar()
                
                pantalla.screen.blit(self.imagen, self.pos)

                #Hitboxes
                py.draw.circle(pantalla.screen, (0, 0, 0), self.circle_center, self.circle_radius, 2)
                py.draw.rect(pantalla.screen, (255, 0, 0), self.hitbox)
                py.draw.rect(pantalla.screen, (255, 0, 0), self.hitbox_ataque)

            if self.start:
                self.temp = [n for n in pantalla.pos]
                self.start = False

        if tipo_juego == "dos_jugadores":
            if jugador == "Jugador 1":
                pass
            if jugador == "Jugador 2":
                pass
        
        
if  __name__ == "__main__":
    exec(open("Juego.py").read())
        
