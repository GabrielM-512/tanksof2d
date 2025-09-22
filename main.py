import pygame
import sys
import math

pygame.init()

screen = pygame.display.set_mode((1920, 1080))
clock = pygame.time.Clock()

square = pygame.rect.Rect(0, 0, 100, 100)

square_gfx_template = pygame.image.load('./assets/PNG/Hulls_Color_D/Hull_02.png').convert_alpha()

square_gfx = square_gfx_template

while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT: # spiel verlassen
			pygame.quit()
			sys.exit()
		elif event.type == pygame.KEYDOWN: # gucken, ob ESC gedrückt
			if event.key == pygame.K_ESCAPE:
				pygame.quit()
				sys.exit()

	mouse_pos = pygame.mouse.get_pos()
	
	# square bewegen
	keys = pygame.key.get_pressed()
	
	if keys[pygame.K_a]:
		square.x -= 10
	if keys[pygame.K_d]:
		square.x += 10
	if keys[pygame.K_s]:
		square.y += 10
	if keys[pygame.K_w]:
		square.y -= 10

	# visual square drehen
	
		
	
		
	# auf den bildschirm zeichnen
	screen.fill((0, 0, 0))
	screen.blit(square_gfx, square)
	
	pygame.display.update()
	
	# framerate limitieren
	clock.tick(60)
	