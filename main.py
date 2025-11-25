import pygame
import warnings

pygame.init()

from src.system.GameManager import GameManager
from src.objects.Tank import Tank
from src.system.jsonreader import parse_config

game_manager = None

def main() -> None:
	global game_manager
	config = parse_config()

	clock = pygame.time.Clock()

	tank = Tank(config["playercolor"], is_local=True)
	tank.rect.center = (config["resolution"]["width"] // 2, config["resolution"]["height"] // 2)

	othertank = Tank(col=config["othercolor"])
	othertank.rect.center = (config["resolution"]["width"] // 2, config["resolution"]["height"] // 2)

	game_manager = GameManager(ip=config["connection"]["IP"], port=config["connection"]["PORT"], tank_object=tank, other_tank=othertank)
	game_manager.create_window(config["resolution"]["width"], config["resolution"]["height"], "Tank 2d")

	game_manager.senddict.clear()
	game_manager.senddict["actions"] = []

	delta_time = 0
	timer = 2000
	framecount = 0

	loading_screen = pygame.image.load("assets/loadingScreen.png").convert()
	loading_screen = pygame.transform.smoothscale(
		loading_screen,
		(config["resolution"]["width"], config["resolution"]["height"])
	)

	while timer > 0:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					game_manager.kill()


		game_manager.screen.blit(loading_screen, (0, 0))
		pygame.display.update()
		delta_time = clock.tick(120)
		timer -= delta_time

	game_manager.senddict["actions"].append("playerLoadedIn")
	game_manager.update(framecount,120)


	while True:
		game_manager.screen.fill((30,30,30))

		if game_manager.TanksLoadedIn:
			if framecount == 1: # ensure we have already loaded in the tanks properly
				game_manager.reset()

			game_manager.update(framecount, delta_time)

			pygame.display.update()

			delta_time = clock.tick(120)

			framecount += 1

		else:
			game_manager.handle_events()

			text_font = pygame.font.Font(None, 50)
			text_surface = text_font.render("Waiting for other player to load in...", True, (255, 255, 255))
			text_rect = text_surface.get_rect(center=(config["resolution"]["width"] // 2, config["resolution"]["height"] // 2))
			game_manager.screen.blit(text_surface, text_rect)

			ip_text_surface = text_font.render(f"Connected Server Address: {config['connection']['IP']}", True, (255, 255, 255))
			ip_text_rect = ip_text_surface.get_rect(center=(config["resolution"]["width"] // 2, config["resolution"]["height"] // 2 + 50))
			game_manager.screen.blit(ip_text_surface, ip_text_rect)

			pygame.display.update()


if __name__ == "__main__":
	try:
		main()
	except KeyboardInterrupt:
		warnings.warn("exited from keyboard interrupt", UserWarning)
		# noinspection PyUnresolvedReferences
		game_manager.kill()
	except Exception as e:
		print(f"Fatal Error: {e}")
