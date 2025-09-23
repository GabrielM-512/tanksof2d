import math
import pygame

from src.objects.Hitbox import Hitbox

from src.objects.Shooting import Bullet





def pos_after_rot(point, angle, pivot):

    x, y = point[0], point[1]
    angle_rad = math.radians(angle)


    return [

        pivot[0] + (x - pivot[0]) * math.cos(angle_rad) - (y - pivot[1]) * math.sin(angle_rad),
        pivot[1] + (x - pivot[0]) * math.sin(angle_rad) + (y-pivot[1]) * math.cos(angle_rad)

    ]

class Tank:

    def __init__(self):


        self.icon_base = pygame.image.load("assets/PNG/Hulls_Color_D/Hull_02.png")
        self.turret_base_icon = pygame.image.load("assets/PNG/Weapon_Color_D/Gun_02.png")

        self.rect = self.icon_base.get_rect()

        self.base_chassis_connect_point = (0, 22)
        self.base_turret_connect_point = (42, 147)

        self.chassis_connection_point = self.base_chassis_connect_point
        self.turret_connection_point = self.base_turret_connect_point

        self.icon = self.icon_base.__copy__()
        self.turret_icon = self.turret_base_icon.__copy__()

        self.chassis_angle : float = 0
        self.turret_angle : float = 0

        self.chassis_angle_rad = 0
        self.turret_angle_rad = 0

        self.hitbox = Hitbox(self.icon, 10, 10)
        self.bullets = []
        self.health = 100
        self.maxBullets = 5

        self.offsetx = self.hitbox.x
        self.offsety = self.hitbox.y

    def move(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.hitbox.y -= 5
            self.rect.y -= 5
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.hitbox.y += 5
            self.rect.y += 5
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.hitbox.x -= 5
            self.rect.x -= 5
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.hitbox.x += 5
            self.rect.x += 5
        if pygame.mouse.get_pressed()[0]:
            self.shoot(pygame.mouse.get_pos())
        if keys[pygame.K_q]:
            self.chassis_angle += 5
        elif keys[pygame.K_e]:
            self.chassis_angle -= 5
    
    def shoot(self,pos):
        #bullet = Bullet(pos)
        pass

    def draw(self, screen):
            
            olist = list(self.hitbox.hitbox.outline())
            after_list = []
            for point in olist:
                x = point[0] + self.hitbox.x
                y = point[1] + self.hitbox.y

                after_list.append((x,y))
            
            pygame.draw.polygon(screen,(200,150,150),after_list,0)

            old_pos = self.rect.center

            self.chassis_angle_rad = math.radians(self.chassis_angle)
            self.icon = pygame.transform.rotate(self.icon_base, self.chassis_angle)

            self.rect = self.icon.get_rect()
            self.rect.center = old_pos

            self.chassis_connection_point = pos_after_rot(self.base_chassis_connect_point, -self.chassis_angle, (0, 0))

            self.chassis_connection_point[0] += old_pos[0]
            self.chassis_connection_point[1] += old_pos[1]

            screen.blit(self.icon, self.rect)
            
            pygame.draw.rect(screen, (255, 0, 0), (self.chassis_connection_point, (2, 2)))
            pygame.draw.rect(screen, (0, 255, 0), (self.rect.center, (2, 2)))


    def update(self, screen):
        self.hitbox.x = self.rect.x
        self.hitbox.y = self.rect.y

        self.draw(screen)
        self.hitbox.update(self.icon)
        
        if len(self.bullets) > 0:
            for bullet in self.bullets:
                bullet.update(screen)

