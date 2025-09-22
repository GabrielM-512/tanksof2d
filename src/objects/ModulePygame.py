import pygame 
import sys

class GameManager:
    def createWindow(WIDTH, HEIGHT,DESCRIPTION):
        pygame.init()
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(DESCRIPTION)
        return screen
    def defineEvents():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
    def playerInputs(player):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            player.y -= 5
        if keys[pygame.K_DOWN]:
            player.y += 5
        if keys[pygame.K_LEFT]:
            player.x -= 5
        if keys[pygame.K_RIGHT]:
            player.x += 5
