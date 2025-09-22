import pygame
import sys
import math
from src.objects.ModulePygame import GameManager
from src.objects.Tank import Tank

pygame.init()

screen = GameManager.createWindow(1440,900,"Tank 2d")
clock = pygame.time.Clock()

tank = Tank()

gameManager = GameManager(tank, "localhost")

tanknpc = Tank()

while True:
	GameManager.defineEvents()

	mouse_pos = pygame.mouse.get_pos()
	
	screen.fill((30,30,30))

	tank.move()
	tank.update(screen)

	tanknpc.move()
	tanknpc.update(screen)

	if tank.hitbox.collides(tanknpc.hitbox):
		pass
	pygame.display.update()
	
	clock.tick(60)
	