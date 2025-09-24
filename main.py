import pygame
import sys
import warnings

from src.system.GameManager import GameManager
from src.objects.Tank import Tank
from src.system.jsonreader import parse_config

def main():
	config = parse_config()

	pygame.init()

	clock = pygame.time.Clock()

	gameManager = GameManager(ip=config["connection"]["IP"], port=config["connection"]["PORT"])

	tank = Tank(config["playercolor"])
	gameManager.tank = tank

	othertank = Tank(col=config["othercolor"])
	gameManager.othertank = othertank

	gameManager.create_window(1280, 720, "Tank 2d")

	gameManager.senddict.clear()
	gameManager.senddict["actions"] = []

	framecount = 0

	while True:
		gameManager.handle_events()

		gameManager.screen.fill((30,30,30))
		gameManager.update(framecount)

		pygame.display.update()

		dT = clock.tick(120)
		fps = clock.get_fps()

		framecount += 1


if __name__ == "__main__":
	try:
		main()
	except KeyboardInterrupt:
		warnings.warn("exited from keyboard interrupt", UserWarning)
		sys.exit(0)