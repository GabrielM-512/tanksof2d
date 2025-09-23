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
    
    def defineEvents():
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()

    def update(self, screen):

        self.handle_input()
        self.tank.update(screen)

    def handle_input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.tank.rect.y -= 5
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.tank.rect.y += 5
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.tank.rect.x -= 5
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.tank.rect.x += 5
        if keys[pygame.K_q]:
            self.tank.chassis_angle += 5
        elif keys[pygame.K_e]:
            self.tank.chassis_angle -= 5

        if pygame.mouse.get_pressed()[0]:
            self.tank.shoot(pygame.mouse.get_pos())

        pos = pygame.mouse.get_pos()
        try:
            angle = math.degrees(math.atan((pos[0] - self.tank.chassis_connection_point[0]) / (pos[1] - self.tank.chassis_connection_point[1])))
            if pos[1] > self.tank.chassis_connection_point[1]:
                angle += 180
        except ZeroDivisionError:
            angle = 0
        
        self.tank.turret_angle = angle
        
