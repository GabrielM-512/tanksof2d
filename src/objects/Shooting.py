import pygame
import math
from src.objects.Hitbox import Hitbox

class Bullet:
    def __init__(self, parent, nPos, mPos, ang):
        self.parent = parent

        self.icon_base = pygame.image.load("assets/PNG/Effects/Medium_Shell.png")
        self.icon_display = self.icon_base.__copy__()

        self.hitbox = Hitbox(self.icon_display, nPos[0], nPos[1])

        self.mx = mPos[0]
        self.my = mPos[1]

        self.speed = 50
        self.angle = ang

        self.length = 500

        self.vx = self.speed * math.sin(math.radians(self.angle))
        self.vy = self.speed * math.cos(math.radians(self.angle))

    def update(self, screen : pygame.display):
        self.hitbox.x -= self.vx
        self.hitbox.y -= self.vy

        self.length -= self.speed
        if self.length <= 0:
            self.destroy()

        self.hitbox.update(self.icon_display)


        self.icon_display = pygame.transform.rotate(self.icon_base, self.angle)
        screen.blit(self.icon_display, (self.hitbox.x - 64, self.hitbox.y - 64))

    def destroy(self):
        if self in self.parent:
            self.parent.remove(self)
        self.parent = None