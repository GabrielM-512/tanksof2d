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

	loadingScreen = pygame.image.load("assets/loadingScreen.png").convert()
	loadingScreen = pygame.transform.smoothscale(
		loadingScreen,
		(config["resolution"]["width"], config["resolution"]["height"])
	)
	game_manager.screen.blit(loadingScreen, (0,0))
	pygame.display.update()
	pygame.time.wait(2000)
	game_manager.senddict["actions"].append("playerLoadedIn")
	game_manager.update(framecount,120)
	while True:
		game_manager.screen.fill((30,30,30))
		if game_manager.TanksLoadedIn:
			game_manager.update(framecount, delta_time)

			pygame.display.update()

			delta_time = clock.tick(120)
			fps = clock.get_fps()

			framecount += 1
		else:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit(0)
				elif event.type == pygame.KEYDOWN:
					if event.key == pygame.K_ESCAPE:
						pygame.quit()
						sys.exit(0)

			text_font = pygame.font.Font(None, 50)
			text_surface = text_font.render("Waiting for other player to load in...", True, (255, 255, 255))
			text_rect = text_surface.get_rect(center=(config["resolution"]["width"] // 2, config["resolution"]["height"] // 2))
			game_manager.screen.blit(text_surface, text_rect)
			pygame.display.update()


if __name__ == "__main__":
	try:
		main()
	except KeyboardInterrupt:
		warnings.warn("exited from keyboard interrupt", UserWarning)
		sys.exit(0)