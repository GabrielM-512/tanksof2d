import pygame
from src.system.GameManager import GameManager
from src.objects.Tank import Tank
from src.system.ConnectionManager import ConnectionManager

import socket
hostname = socket.gethostname()
IPAddr = socket.gethostbyname(hostname)


pygame.init()

clock = pygame.time.Clock()

gameManager = GameManager(ip=IPAddr, port=5000)

tank = Tank()
gameManager.tank = tank

othertank = Tank(col="Red")
gameManager.othertank = othertank

gameManager.create_window(1280, 720, "Tank 2d")

while True:
	gameManager.handle_events()

	mouse_pos = pygame.mouse.get_pos()
	
	gameManager.screen.fill((30,30,30))
	gameManager.update()

	pygame.display.update()
	
	dT = clock.tick(120)
	fps = clock.get_fps()
	