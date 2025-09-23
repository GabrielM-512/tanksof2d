import pygame 
import sys
import math

from src.objects.Tank import Tank

class GameManager:
    def __init__(self, tankobject : Tank, ip: str):
        self.tank = tankobject
        self.serverIP = ip

    def createWindow(WIDTH, HEIGHT,DESCRIPTION):
        pygame.init()
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(DESCRIPTION)
        return screen
    
    def defineEvents(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.tank.maxBullets > len(self.tank.bullets):
                    self.tank.shoot(pygame.mouse.get_pos())



    def update(self, screen):

        self.handle_input()
        self.tank.update(screen)

    def handle_input(self):
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
        
