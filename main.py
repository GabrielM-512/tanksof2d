import pygame
import sys
import warnings

pygame.init()

from src.system.GameManager import GameManager
from src.objects.Tank import Tank
from src.system.jsonreader import parse_config

def main():
	config = parse_config()

	clock = pygame.time.Clock()

	tank = Tank(config["playercolor"], is_local=True)
	tank.rect.center = (config["resolution"]["width"] // 2, config["resolution"]["height"] // 2)
	othertank = Tank(col=config["othercolor"])
	othertank.rect.center = (config["resolution"]["width"] // 2, config["resolution"]["height"] // 2)

	game_manager = GameManager(ip=config["connection"]["IP"], port=config["connection"]["PORT"], tankobject=tank, other_tank=othertank)
	game_manager.create_window(config["resolution"]["width"], config["resolution"]["height"], "Tank 2d")

	game_manager.senddict.clear()
	game_manager.senddict["actions"] = []

	delta_time = 0

	framecount = 0

	while True:
		game_manager.screen.fill((30,30,30))
		game_manager.update(framecount, delta_time)

		pygame.display.update()

		delta_time = clock.tick(120)
		fps = clock.get_fps()

		framecount += 1


if __name__ == "__main__":
	try:
		main()
	except KeyboardInterrupt:
		warnings.warn("exited from keyboard interrupt", UserWarning)
		sys.exit(0)