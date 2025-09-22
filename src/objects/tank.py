import pygame
import math
from src.objects.Hitbox import Hitbox
from src.objects.Shooting import Bullet
import numpy as np


class Tank:
    def __init__(self):
        self.icon_base = pygame.image.load("assets/PNG/Hulls_Color_D/Hull_02.png")
        self.icon_display = self.icon_base
        self.chasis_icon = pygame.image.load("assets/PNG/Weapon_Color_D/Gun_01.png")
        self.chasis_display = self.icon_base
        self.rect = Hitbox(self.icon_display,10,10)
        self.bullets = []
        self.health = 100
        self.maxBullets = 5
        self.angle = 0
        self.chasisPosX,self.chasisPosY = self.find_black_circle_center("assets/PNG/Hulls_Color_D/Hull_02.png")

    def move(self):
        self.turn_turret()
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

    def turn_turret(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        tank_center_x = self.rect.x + self.chasisPosX
        tank_center_y = self.rect.y + self.chasisPosY
        delta_x = mouse_x - tank_center_x
        delta_y = mouse_y - tank_center_y
        self.angle = math.degrees(math.atan2(-delta_y, delta_x)) - 90
        self.chasis_display = pygame.transform.rotate(self.chasis_icon, self.angle)

    def shoot(self,pos):
        bullet = Bullet(self.bullets,(self.rect.x,self.rect.y),pos,self.angle)
        self.bullets.append(bullet)
    
    def draw(self, screen):
        #print("sigma")
        #olist = self.rect.hitbox.outline()
        #pygame.draw.polygon(screen,(200,150,150),olist,0)
        screen.blit(self.icon_display, (self.rect.x, self.rect.y))
        pygame.draw.circle(screen, (255, 0, 0), (self.rect.x + self.chasisPosX, self.rect.y + self.chasisPosY), 5)
        print(self.find_black_circle_center("assets/PNG/Hulls_Color_D/Hull_02.png"))

        screen.blit(
            self.chasis_display,
            (
                self.chasisPosX - self.chasis_display.get_width() // 2 + self.rect.x,
                self.chasisPosY - self.chasis_display.get_height() // 2 + self.rect.y -50
            )
        )

    def update(self, screen):
        self.draw(screen)
        self.rect.update(self.icon_display)
        if len(self.bullets) > 0:
            for bullet in self.bullets:
                bullet.update(screen)

    def find_black_circle_center(self, image_path):
        surf = pygame.image.load(image_path).convert_alpha()
        arr = pygame.surfarray.array3d(surf)

        mask = np.all(arr < [20, 20, 20], axis=2) 
        ys, xs = np.where(mask)

        if len(xs) == 0 or len(ys) == 0:
            raise ValueError("No black dot found!")

        cx = int(xs.mean())
        cy = int(ys.mean()) + 23
        return cx, cy
