import pygame
class Hitbox:
    def __init__(self,source,x,y):
        self.hitbox = pygame.mask.from_surface(source)
        self.x = x
        self.y = y

    def update(self, source):
        self.hitbox = pygame.mask.from_surface(source)

    def collides(self, pastHitbox):
        return self.hitbox.overlap_area(pastHitbox.hitbox, (pastHitbox.x - self.x, pastHitbox.y - self.y)) > 0