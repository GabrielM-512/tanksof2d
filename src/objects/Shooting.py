import pygame
import math
from src.objects.Hitbox import Hitbox

class Bullet:
    def __init__(self,parent,nPos,mPos,ang):
        self.parent = parent
        self.icon_base = pygame.image.load("assets/PNG/Effects/Medium_Shell.png")
        self.icon_display = self.icon_base
        self.bullet = Hitbox(self.icon_display,nPos[0],nPos[1])
        self.mx = mPos[0]
        self.my = mPos[1]
        self.speed = 50
        self.angle = ang
        self.vx = 0
        self.vy = 0

    def calcBullet(self):
        dx, dy = self.mx - self.bullet.x, self.my - self.bullet.y
        length = math.hypot(dx,dy)
        if length <= self.speed:  # or some small threshold
            self.destroy()
        else:
            if length == 0:
                length = 1
            dir_x = dx / length
            dir_y = dy / length
            self.vx = dir_x * self.speed
            self.vy = dir_y * self.speed
            self.icon_display = pygame.transform.rotate(self.icon_base,self.angle)

    def update(self,screen:pygame.display):
        self.bullet.update(self.icon_display)
        self.bullet.x -= self.speed * math.sin(math.radians(self.angle))
        self.bullet.y -= self.speed * math.cos(math.radians(self.angle))
        self.calcBullet()
        screen.blit(self.icon_display, (self.bullet.x - 64, self.bullet.y - 64))

    def destroy(self):
        if self in self.parent:
            self.parent.remove(self)
        self.parent = None