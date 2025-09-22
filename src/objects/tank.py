import pygame
import math

class tank:

    def __init__(self):
        self.rect = pygame.rect.Rect()
        #self.icon_base = pygame.image.load()
        self.icon_display = self.icon_base

    def move(self):
        pass

    def turn_turret(self):
        try:
            mouse_pos = pygame.mouse.get_pos
            rot_degree = math.atan((mouse_pos[0] - self.rect.centerx) / (mouse_pos[1] - square.centery))
            if mouse_pos[1] - self.rect.centery > 0:
                rot_degree += math.pi
                
            square_gfx = pygame.transform.rotate(square_gfx_template, rot_degree * 180 / math.pi)
        except ZeroDivisionError:
            if mouse_pos[0] - square.centerx < 0:
                square_gfx = pygame.transform.rotate(square_gfx_template, 90)
            elif mouse_pos[0] - square.centerx > 0:
                square_gfx = pygame.transform.rotate(square_gfx_template, -90)

    def shoot(self):
        pass
    
    def update(self):
        self.move()
