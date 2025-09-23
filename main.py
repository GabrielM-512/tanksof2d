import pygame
from src.system.GameManager import GameManager
from src.objects.Tank import Tank
from src.system.ConnectionManager import ConnectionManager

pygame.init()
ConnectionManager
clock = pygame.time.Clock()

gameManager = GameManager("localhost")

tank = Tank()
gameManager.tank = tank

gameManager.create_window(1920, 1080, "Tank 2d")

while True:
	gameManager.handle_events()

	mouse_pos = pygame.mouse.get_pos()
	
	gameManager.screen.fill((30,30,30))
	gameManager.update()

	pygame.display.update()
	
	dT = clock.tick(120)
	fps = clock.get_fps()
	