import pygame
from src.objects.ModulePygame import GameManager
from src.objects.Tank import Tank

pygame.init()

screen = GameManager.createWindow(1440,900,"Tank 2d")
clock = pygame.time.Clock()

tank = Tank()

gameManager = GameManager(tank, "localhost")

while True:
	gameManager.defineEvents()

	mouse_pos = pygame.mouse.get_pos()
	
	screen.fill((30,30,30))

	gameManager.update(screen)

	pygame.display.update()
	
	dT = clock.tick(120)
	fps = clock.get_fps()
	