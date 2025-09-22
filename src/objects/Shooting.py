import pygame
import math
from src.objects.Hitbox import Hitbox

class Bullet:
    def __init__(self,parent,tPos,mPos,ang):
        self.parent = parent
        self.icon_base = pygame.image.load("assets/PNG/Effects/Medium_Shell.png")
        self.icon_display = self.icon_base
        self.bullet = Hitbox(self.icon_display,tPos[0],tPos[1])
        self.mx = mPos[0]
        self.my = mPos[1]
        self.speed = 5
        self.angle = ang
        self.vx = 0
        self.vy = 0

    def calcBullet(self):
        dx, dy = self.mx - self.bullet.x, self.my - self.bullet.y
        if dx <= 0 and dy <= 0:
            self.destroy()
        length = math.hypot(dx, dy)
        if length == 0:
            length = 1
        dir_x, dir_y = dx / length, dy / length
        speed = 10

        self.vx = dir_x * speed
        self.vy = dir_y * speed

    def update(self,screen:pygame.display):
        self.bullet.x += self.vx
        self.bullet.y += self.vy
        screen.blit(self.icon_display, (self.bullet.x - 64, self.bullet.y - 64))
        self.calcBullet()

    def destroy(self):
        if self in self.parent:
            self.parent.remove(self)
        self.parent = None