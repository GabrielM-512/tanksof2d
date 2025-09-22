import pygame
import math
from src.objects.Hitbox import Hitbox
from src.objects.Shooting import Bullet
class Tank:
    def __init__(self):
        self.icon_base = pygame.image.load("assets/PNG/Weapon_Color_D/Gun_02.png")
        self.icon_display = self.icon_base
        self.rect = Hitbox(self.icon_display,10,10)
        self.bullets = []
        self.health = 100
        self.maxBullets = 5
        self.angle = 0

    def move(self):
        self.turn_turret(0)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.rect.y -= 5
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.rect.y += 5
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.rect.x -= 5
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.rect.x += 5
        if pygame.mouse.get_pressed()[0]:
            self.shoot(pygame.mouse.get_pos())

    def turn_turret(self, angle):
        try:
            mouse_pos = pygame.mouse.get_pos()
            newRect = self.icon_display.get_rect(center=(self.rect.x + self.icon_display.get_width() // 2, self.rect.y + self.icon_display.get_height() // 2))
            rot_degree = math.atan((mouse_pos[0] - newRect.centerx) / (mouse_pos[1] - newRect.centery))
            if mouse_pos[1] - newRect.centery > 0:
                rot_degree += math.pi
                
            self.icon_display = pygame.transform.rotate(self.icon_base, rot_degree * 180 / math.pi)
            self.angle = rot_degree
        except ZeroDivisionError:
            if mouse_pos[0] - newRect.centerx < 0:
                self.icon_display = pygame.transform.rotate(self.icon_base, 90)
                self.angle = 90
            elif mouse_pos[0] - newRect.centerx > 0:
                self.icon_display = pygame.transform.rotate(self.icon_base, -90)
                self.angle = -90

    def shoot(self,pos):
        bullet = Bullet(self.bullets,(self.rect.x,self.rect.y),pos,self.angle)
        self.bullets.append(bullet)
    
    def draw(self, screen):
        #print("sigma")
        #olist = self.rect.hitbox.outline()
        #pygame.draw.polygon(screen,(200,150,150),olist,0)
        screen.blit(self.icon_display, (self.rect.x, self.rect.y))

    def update(self, screen):
        self.rect.update(self.icon_display)
        if len(self.bullets) > 0:
            for bullet in self.bullets:
                bullet.update(screen)
        self.draw(screen)
