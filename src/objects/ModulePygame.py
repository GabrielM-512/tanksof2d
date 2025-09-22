import pygame 
import sys

class GameManager:
    def __init__(self, tankobject, ip: str):
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