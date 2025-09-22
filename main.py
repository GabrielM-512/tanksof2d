import pygame
import sys
import math
from src.objects.ModulePygame import GameManager

pygame.init()

screen = GameManager.createWindow(1440,900,"Tank 2d")
clock = pygame.time.Clock()

square = pygame.rect.Rect(0, 0, 100, 100)

square_gfx_template = pygame.image.load('./assets/PNG/Hulls_Color_D/Hull_02.png').convert_alpha()

square_gfx_template2 = pygame.Surface((100,100))
square_gfx_template2.fill((255,255,255))

while True:
	GameManager.defineEvents()

	mouse_pos = pygame.mouse.get_pos()
	
	screen.fill((0, 0, 0))
	screen.blit(square_gfx_template, square)
	screen.blit(square_gfx_template2, square)
	
	pygame.display.update()
	
	# framerate limitieren
	clock.tick(60)
	