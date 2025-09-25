import pygame
import math
from src.system.Hitbox import Hitbox

class Bullet:
    def __init__(self, parent, nPos, ang):
        self.parent = parent

        self.icon_base = pygame.image.load("assets/PNG/Effects/Medium_Shell.png")
        self.icon_display = self.icon_base.__copy__()

        self.hitbox = Hitbox(self.icon_display, nPos[0], nPos[1])
        self.rect = self.icon_base.get_rect()

        self.rect.centerx = nPos[0]
        self.rect.centery = nPos[1]

        self.speed = 15
        self.angle = ang

        self.length = 5000

        self.vx = self.speed * math.sin(math.radians(self.angle))
        self.vy = self.speed * math.cos(math.radians(self.angle))

    def update(self, screen : pygame.surface.Surface):
        self.rect.x -= self.vx
        self.rect.y -= self.vy

        self.hitbox.x = self.rect.x
        self.hitbox.y = self.rect.y

        self.length -= self.speed
        if self.length <= 0:
            self.destroy()

        pos_old = self.rect.center

        self.icon_display = pygame.transform.rotate(self.icon_base, self.angle)

        self.rect = self.icon_display.get_rect()
        self.rect.center = pos_old


        self.hitbox.update(self.icon_display)

        screen.blit(self.icon_display, self.rect)

        """olist = list(self.hitbox.hitbox.outline())

        after_list = []
        for point in olist:
            x = point[0] + self.hitbox.x
            y = point[1] + self.hitbox.y

            after_list.append((x, y))

        pygame.draw.polygon(screen, (200, 150, 150), after_list, 0)"""

    def collision(self, objdict):
        for obj in objdict.values():
            if obj is not self and obj is not self.parent and hasattr(obj, "hitbox"):
                if self.hitbox.collides(obj.hitbox):
                    self.parent.callback(obj, self)

    def destroy(self):
        if self in self.parent.bullets:
            self.parent.bullets.remove(self)
        self.parent = None