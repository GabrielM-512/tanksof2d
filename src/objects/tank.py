import pygame
import math

class Tank:

    def __init__(self):
        self.rect = pygame.rect.Rect()
        self.icon_base = pygame.image.load("assets/PNG/Hulls_Color_A/Hull_02.png")
        self.icon_display = self.icon_base

    def move(self):
        pass

    def turn_turret(self):
        try:
            mouse_pos = pygame.mouse.get_pos()
            rot_degree = math.atan((mouse_pos[0] - self.rect.centerx) / (mouse_pos[1] - self.rect.centery))
            if mouse_pos[1] - self.rect.centery > 0:
                rot_degree += math.pi
                
            square_gfx = pygame.transform.rotate(self.icon_base, rot_degree * 180 / math.pi)

        except ZeroDivisionError:
            if mouse_pos[0] - self.rect.centerx < 0:
                square_gfx = pygame.transform.rotate(self.icon_base, 90)
            elif mouse_pos[0] - self.rect.centerx > 0:
                square_gfx = pygame.transform.rotate(self.icon_base, -90)

    def shoot(self):
        pass
    
    def draw(self, screen : pygame.display):
        screen.blit(self.icon_display, self.rect)
