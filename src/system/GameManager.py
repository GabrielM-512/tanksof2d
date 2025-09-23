import pygame 
import sys
import math

from src.system.ConnectionManager import ConnectionManager
from src.objects.Tank import Tank

class GameManager:
    def __init__(self, ip: str = "localhost", port : int = "5000", tankobject : Tank = None):
        self.tank = tankobject

        self.screen = None
        self.connection = ConnectionManager(host=ip, port=port, callback=self.handle_connection)

        try:
            self.connection.connect()
        except:
            print("No connection achieved, launched in single-player testing mode")


    def create_window(self, width, height, description):
        pygame.init()
        screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption(description)
        self.screen = screen


    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                self.kill()
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.tank.maxBullets > len(self.tank.bullets):
                    self.tank.shoot(pygame.mouse.get_pos())



    def update(self):
        if self.screen is None:
            raise Exception("Screen was not defined")
        self.handle_input()
        self.tank.update(self.screen)


    def handle_input(self):
        if self.tank is None:
            return

        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.tank.rect.x -= self.tank.MOVEMENT_SPEED * math.sin(math.radians(self.tank.chassis_angle))
            self.tank.rect.y -= self.tank.MOVEMENT_SPEED * math.cos(math.radians(self.tank.chassis_angle))
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.tank.rect.x += self.tank.MOVEMENT_SPEED * math.sin(math.radians(self.tank.chassis_angle))
            self.tank.rect.y += self.tank.MOVEMENT_SPEED * math.cos(math.radians(self.tank.chassis_angle))
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.tank.chassis_angle += self.tank.ROTATION_SPEED
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.tank.chassis_angle -= self.tank.ROTATION_SPEED


        pos = pygame.mouse.get_pos()
        try:
            angle = math.degrees(math.atan((pos[0] - self.tank.global_connect_point[0]) / (pos[1] - self.tank.global_connect_point[1])))
            if pos[1] > self.tank.global_connect_point[1]:
                angle += 180

        except ZeroDivisionError:
            if pos[0] > self.tank.global_connect_point[0]:
                angle = -90
            else:
                angle = 90
        
        self.tank.turret_angle = angle

    def handle_connection(self, msg : dict):
        pass

    def kill(self):
        self.connection.close()