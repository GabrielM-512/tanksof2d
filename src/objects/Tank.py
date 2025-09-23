import math
import pygame

from src.system.Hitbox import Hitbox

from src.objects.Bullet import Bullet


"""
Class for representing the Tanks from both the local player, other players and NPCs.
Movement is handled by the GameManager class.
"""


def pos_after_rot(point, angle, pivot):

    x, y = point[0], point[1]
    angle_rad = math.radians(angle)

    return [

        pivot[0] + (x - pivot[0]) * math.cos(angle_rad) - (y - pivot[1]) * math.sin(angle_rad),
        pivot[1] + (x - pivot[0]) * math.sin(angle_rad) + (y-pivot[1]) * math.cos(angle_rad)

    ]


def transparent_surface(width, height):
    surface = pygame.Surface((width, height), pygame.SRCALPHA)
    surface.fill((0, 0, 0, 0))
    return surface


class Tank:


    MOVEMENT_SPEED = 5
    ROTATION_SPEED = 1

    BULLET_SPAWN_OFFSET = 20

    def __init__(self):


        self.chassis_display_base = pygame.image.load("assets/PNG/Hulls_Color_D/Hull_02.png")
        self.turret_base_icon = pygame.image.load("assets/PNG/Weapon_Color_D/Gun_01.png")
        self.final_display_base = transparent_surface(self.chassis_display_base.get_width() + 200, self.chassis_display_base.get_height() + 200)

        self.rect = self.chassis_display_base.get_rect()
        self.turretRect = self.turret_base_icon.get_rect()

        self.base_chassis_connect_point = (0, 22)
        self.base_turret_connect_point = (0, 54)
        self.nozzle_position = (0, 100)

        self.chassis_connection_point = self.base_chassis_connect_point
        self.turret_connection_point = self.base_turret_connect_point

        self.final_display = self.final_display_base.__copy__()
        self.chassis_display = self.chassis_display_base.__copy__()
        self.turret_icon = self.turret_base_icon.__copy__()

        self.chassis_angle : float = 0
        self.turret_angle : float = 0

        self.hitbox = Hitbox(self.chassis_display, 10, 10)
        self.bullets = []
        self.health = 100
        self.maxBullets = 1000

        self.offsetx = self.hitbox.x
        self.offsety = self.hitbox.y
    
        self.global_connect_point = (0,0)

    def shoot(self,pos):
        bullet = Bullet(self.bullets, self.nozzle_position, self.turret_angle)
        self.bullets.append(bullet)
        
    def draw(self, screen):
            


            self.final_display = self.final_display_base.__copy__()

            old_pos = self.rect.center

            self.chassis_display = pygame.transform.rotate(self.chassis_display_base, self.chassis_angle)

            self.rect = self.chassis_display.get_rect()
            self.rect.center = old_pos

            self.chassis_connection_point = pos_after_rot(self.base_chassis_connect_point, -self.chassis_angle, (0, 0))

            self.chassis_connection_point[0] += old_pos[0]
            self.chassis_connection_point[1] += old_pos[1]

            self.final_display.blit(self.chassis_display, (100, 100))

            self.turret_icon = pygame.transform.rotate(self.turret_base_icon, self.turret_angle)

            self.turretRect = self.turret_icon.get_rect()

            turr_connect_point = pos_after_rot(self.base_turret_connect_point, -self.turret_angle, (0, 0))



            offsetx = self.chassis_connection_point[0] - self.rect.centerx
            offsety = self.chassis_connection_point[1] - self.rect.centery

            local_chassis_x = self.chassis_connection_point[0] - self.rect.x
            local_chassis_y = self.chassis_connection_point[1] - self.rect.y

            self.turretRect.center = (local_chassis_x - offsetx - turr_connect_point[0] + 100, local_chassis_y - offsety - turr_connect_point[1] + 100)
            

            self.final_display.blit(self.turret_icon, (offsetx+self.turretRect.x, offsety+self.turretRect.y))

            self.global_connect_point = (local_chassis_x + 100 + self.rect.x, local_chassis_y + 100 + self.rect.y)
        
            

            local_nozzle_pos = pos_after_rot((0, -160 - Tank.BULLET_SPAWN_OFFSET), -self.turret_angle, (0, 0))
            local_nozzle_pos = (local_nozzle_pos[0] + self.global_connect_point[0], local_nozzle_pos[1] + self.global_connect_point[1])
            self.nozzle_position = local_nozzle_pos

            pygame.draw.rect(screen, (255, 0, 0,), (self.nozzle_position, (2, 2)))

            screen.blit(self.final_display, self.rect)


    def update(self, screen):
        self.hitbox.x = self.rect.x
        self.hitbox.y = self.rect.y

        self.draw(screen)
        self.hitbox.update(self.final_display)

        """olist = list(self.hitbox.hitbox.outline())
        after_list = []
        for point in olist:
            x = point[0] + self.hitbox.x
            y = point[1] + self.hitbox.y

            after_list.append((x, y))

        pygame.draw.polygon(screen, (200, 150, 150), after_list, 0)"""

        if len(self.bullets) > 0:
            for bullet in self.bullets:
                bullet.update(screen)
