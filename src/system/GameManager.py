import pygame 
import sys
import math

import warnings

from src.system.ConnectionManager import ConnectionManager
from src.objects.Tank import Tank
from src.objects.Bullet import Bullet

class GameManager:

    UPDATEDURATION = 1

    def __init__(self, ip: str = "localhost", port : int = "5000", tankobject : Tank = None, other_tank : Tank = None):
        self.tank = tankobject
        self.tank.callback = self.hit_handler
        self.othertank = other_tank

        self.old_turret_angle = 0.0

        self.objdict = {
            
        }

        if tankobject is not None:
            self.objdict["selftank"] = tankobject
        if other_tank is not None:
            self.objdict["othertank"] = other_tank

        self.senddict = {}

        self.screen = None
        self.connection = ConnectionManager(host=ip, port=port, callback=self.handle_connection)
        try:
            self.connection.connect()
        except Exception as error:
            print(f"Connection to server failed, launching in Singleplayer: {error}")
            self.connection.offline = True

    def create_window(self, width, height, description):
        pygame.init()
        screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption(description)
        self.screen = screen


    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                self.kill()
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.tank.maxBullets > len(self.tank.bullets):
                    self.tank.shoot()

                if not "shoot" in self.senddict["actions"]:
                    self.senddict["actions"].append("shoot")

                self.senddict["shoot"] = {}
                self.senddict["shoot"]["angle"] = self.tank.turret_angle
                self.senddict["shoot"]["pos"] = self.tank.nozzle_position


    def update(self, framecount):
        if self.screen is None:
            raise Exception("Screen was not defined")
        self.handle_input()
        self.tank.update(self.screen)
        self.othertank.update(self.screen)

        self.tank.collisions(self.objdict)


        if framecount % self.UPDATEDURATION == 0 and len(self.senddict) > 1:
            self.connection.send(self.senddict)
            self.senddict.clear()
            self.senddict["actions"] = []


    def handle_input(self):
        if self.tank is None:
            return

        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.tank.rect.x -= self.tank.MOVEMENT_SPEED * math.sin(math.radians(self.tank.chassis_angle))
            self.tank.rect.y -= self.tank.MOVEMENT_SPEED * math.cos(math.radians(self.tank.chassis_angle))
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.tank.rect.x += self.tank.MOVEMENT_SPEED * math.sin(math.radians(self.tank.chassis_angle))
            self.tank.rect.y += self.tank.MOVEMENT_SPEED * math.cos(math.radians(self.tank.chassis_angle))
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.tank.chassis_angle += self.tank.ROTATION_SPEED
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.tank.chassis_angle -= self.tank.ROTATION_SPEED

        if keys[pygame.K_w] or keys[pygame.K_s] or keys[pygame.K_a] or keys[pygame.K_d] or keys[pygame.K_LEFT] or keys[pygame.K_RIGHT] or keys[pygame.K_UP] or keys[pygame.K_DOWN]:
            if not "move" in self.senddict["actions"]:
                self.senddict["actions"].append("move")
            self.senddict["x"] = self.tank.rect.x
            self.senddict["y"] = self.tank.rect.y

            if not "turn" in self.senddict["actions"]:
                self.senddict["actions"].append("turn")
            self.senddict["angle"] = self.tank.chassis_angle



        pos = pygame.mouse.get_pos()

        try:
            angle = math.degrees(math.atan((pos[0] - self.tank.global_connect_point[0]) / (pos[1] - self.tank.global_connect_point[1])))
            if pos[1] > self.tank.global_connect_point[1]:
                angle += 180

        except ZeroDivisionError:
            if pos[0] > self.tank.global_connect_point[0]:
                angle = -90
            else:
                angle = 90
        
        self.tank.turret_angle = angle

        if self.old_turret_angle != self.tank.turret_angle:
            if not "turn_turret" in self.senddict["actions"]:
                self.senddict["actions"].append("turn_turret")

            self.old_turret_angle = self.tank.turret_angle

            self.senddict["turret_angle"] = self.tank.turret_angle

    def handle_connection(self, msg : dict):
        try:
            actions = msg["actions"]

            for action in actions:
                match action:
                    case "move":
                        self.othertank.rect.x = msg["x"]
                        self.othertank.rect.y = msg["y"]
                    case "turn":
                        self.othertank.chassis_angle = msg["angle"] # seems to lag a little
                    case "turn_turret":
                        self.othertank.turret_angle = msg["turret_angle"]
                    case "shoot":
                        old_angle = self.othertank.turret_angle
                        self.othertank.turret_angle = msg["shoot"]["angle"]

                        self.othertank.shoot(msg["shoot"]["pos"])

                        self.othertank.turret_angle = old_angle
                    case "hit":
                        obj = self.objdict[msg["hitinfo"]["hitobj"]]
                        bullet : Bullet = self.objdict[msg["hitinfo"]["bullet"]]
                        self.objdict.pop(obj)
                        bullet.destroy()

                    case "disconnect":
                        self.connection.offline = True

        except Exception as error:
            print("error in handle_connection(): ", error, msg)

    def hit_handler(self, obj, bullet : Bullet):
        print("hit: ", self, obj, bullet)
        if not self.connection.offline:
            if "hit" not in self.senddict["actions"]:
                self.senddict["actions"].append("hit")
            if "hitinfo" not in self.senddict:
                self.senddict["hitinfo"] = []

            # get the keys for the object and bullet
            bulletkey = [key for key, val in self.objdict.items() if val == bullet]
            objkey = [key for key, val in self.objdict.items() if val == obj]
            if len(bulletkey) > 0 and len(objkey) > 0:
                self.senddict["hitinfo"].append({"hitobject": objkey[0], "bullet": bulletkey[0]})
            else:
                warnings.warn(f"No key found for object: {obj} or bullet: {bullet}", RuntimeWarning)

        try:
            obj.hit(bullet)
        except:
            warnings.warn("error in hit_handler", RuntimeWarning)

        bullet.destroy()
        


    def kill(self):
        self.connection.close()