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

	tank = Tank(config["playercolor"], is_local=True)
	tank.rect.center = (config["resolution"]["width"] // 2 + 100, config["resolution"]["height"] // 2 + 100)
	othertank = Tank(col=config["othercolor"])
	othertank.rect.center = (config["resolution"]["width"] // 2 + 100, config["resolution"]["height"] // 2 + 100)

	gameManager = GameManager(ip=config["connection"]["IP"], port=config["connection"]["PORT"], tankobject=tank, other_tank=othertank)
	gameManager.create_window(config["resolution"]["width"], config["resolution"]["height"], "Tank 2d")

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