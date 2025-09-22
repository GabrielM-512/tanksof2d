import pygame
import math
from src.objects.Hitbox import Hitbox
class Tank:

    def __init__(self, is_player):
        self.icon_base = pygame.image.load("assets/PNG/Hulls_Color_A/Hull_02.png")
        self.icon_display = self.icon_base
        self.rect = Hitbox(self.icon_display,10,10)
        self.is_player = is_player

    def move(self):
        self.turn_turret()
        if self.is_player:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_UP] or keys[pygame.K_w]:
                self.rect.y -= 5
            if keys[pygame.K_DOWN] or keys[pygame.K_s]:
                self.rect.y += 5
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                self.rect.x -= 5
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                self.rect.x += 5

    def turn_turret(self):
        try:
            print("gets called")
            mouse_pos = pygame.mouse.get_pos()
            mask_rect = self.rect.hitbox.get_rect()
            rot_degree = math.atan((mouse_pos[0] - mask_rect.centerx) / (mouse_pos[1] - mask_rect.centery))
            if mouse_pos[1] - mask_rect.centery > 0:
                rot_degree += math.pi
                
            self.icon_display = pygame.transform.rotate(self.icon_base, rot_degree * 180 / math.pi)

        except ZeroDivisionError:
            mask_rect = self.rect.hitbox.get_rect()
            if mouse_pos[0] - mask_rect.centerx < 0:
                self.icon_display = pygame.transform.rotate(self.icon_base, 90)
            elif mouse_pos[0] - mask_rect.centerx > 0:
                self.icon_display = pygame.transform.rotate(self.icon_base, -90)

    def shoot(self):
        pass
    
    def draw(self, screen):
        #print("sigma")
        #olist = self.rect.hitbox.outline()
        #pygame.draw.polygon(screen,(200,150,150),olist,0)
        screen.blit(self.icon_display, (self.rect.x, self.rect.y))


    def update(self, screen):
        self.rect.update(self.icon_display)
        self.draw(screen)