import pygame
import sys
import math
from src.objects.ModulePygame import GameManager

pygame.init()

screen = GameManager.createWindow(1920,1080,"Tank 2d")
clock = pygame.time.Clock()

square = pygame.rect.Rect(0, 0, 100, 100)

square_gfx_template = pygame.image.load('./assets/PNG/Hulls_Color_D/Hull_02.png').convert_alpha()

square_gfx = square_gfx_template

while True:
	GameManager.defineEvents()

	mouse_pos = pygame.mouse.get_pos()
	
	GameManager.playerInputs(square)

	screen.fill((0, 0, 0))
	screen.blit(square_gfx, square)
	
	pygame.display.update()
	
	# framerate limitieren
	clock.tick(60)
	