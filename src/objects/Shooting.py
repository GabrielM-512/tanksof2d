import pygame
from src.objects.Hitbox import Hitbox
class Bullet:
    def __init__(self,pos):
        self.icon_base = pygame.image.load("assets/PNG/Effects/Medium_Shell.png")
        self.icon_display = self.icon_base
        self.bullet = Hitbox(self.icon_display,pos[0],pos[1])
        self.mass = 0.1
    
    def update(self,screen:pygame.display):
        screen.blit(self.icon_display, (self.bullet.x - 64, self.bullet.y - 64))
        print("nothin")

    