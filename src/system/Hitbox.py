import pygame
class Hitbox:
    def __init__(self, source: pygame.Surface, x: int, y: int):
        self.hitbox: pygame.Mask = pygame.mask.from_surface(source, threshold=50)
        self.x: int = x
        self.y: int = y

    def update(self, source: pygame.Surface):
        self.hitbox = pygame.mask.from_surface(source, threshold=50)

    def collides(self, past_hitbox) -> bool:
        return self.hitbox.overlap_area(past_hitbox.hitbox, (past_hitbox.x - self.x, past_hitbox.y - self.y)) > 0