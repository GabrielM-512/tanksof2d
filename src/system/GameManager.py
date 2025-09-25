import pygame 
import sys
import math

import warnings

from src.system.ConnectionManager import ConnectionManager
from src.objects.Tank import Tank
from src.objects.Bullet import Bullet

class GameManager:

    UPDATEFREQUENCY = 1

    def __init__(self, ip: str = "localhost", port : int = "5000", tankobject : Tank = None, other_tank : Tank = None):
        
        self.playerId = None
        self.mode : str = None

        self.shotbullets = 0

        self.tank = tankobject
        self.tank.callback = self.hit_handler

        self.othertank = other_tank
        self.othertankID = None

        self.old_turret_angle = 0.0

        self.objdict = {
            
        }

        self.senddict = {}

        self.screen = None
        self.connection = ConnectionManager(host=ip, port=port, callback=self.handle_connection)

        self.playMode = None

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

    def set_tank_object(self, tank, tank_id):
        self.objdict[f"tank{tank_id}"] = tank

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                self.kill()
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if self.tank.maxBullets > len(self.tank.bullets):
                        bullet = self.tank.shoot(self.objdict)

                        self.objdict[f"{self.playerId}:Bullet:{self.shotbullets}"] = bullet

                        if not "shoot" in self.senddict["actions"]:
                            self.senddict["actions"].append("shoot")

                        self.senddict["shoot"] = {}
                        self.senddict["shoot"]["angle"] = self.tank.turret_angle
                        self.senddict["shoot"]["pos"] = self.tank.nozzle_position
                        self.senddict["shoot"]["id"] = f"{self.playerId}:Bullet:{self.shotbullets}"

                        self.shotbullets += 1

    def update(self, framecount):
        assert isinstance(self.objdict, dict)

        if self.screen is None:
            raise Exception("Screen was not defined")
        self.handle_input()
        self.tank.update(self.screen)
        self.othertank.update(self.screen)

        self.tank.collisions(self.objdict, self.othertankID)


        if framecount % self.UPDATEFREQUENCY == 0 and len(self.senddict) > 1:
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

                        bullet = self.othertank.shoot(self.objdict, pos=msg["shoot"]["pos"])
                        self.objdict[msg["shoot"]["id"]] = bullet

                        self.othertank.turret_angle = old_angle

                    case "hit":
                        print("received hit: ", msg)
                        obj = self.objdict[msg["hitinfo"]["hitObjectKey"]]
                        bullet : Bullet = self.objdict[msg["hitinfo"]["bulletKey"]]

                        obj.hit(bullet)
                        bullet.destroy()

                    case "connect":
                        self.playerId = msg["id"]
                        self.playMode = msg["mode"]
                        #print("connect: ", msg)

                        if self.tank is not None:
                            self.objdict[f"tank:{self.playerId}"] = self.tank
                        else: raise Exception("tank was none on server connect")

                        if self.othertank is not None:
                            if self.playerId == 0:
                                self.objdict["tank:1"] = self.othertank
                            elif self.playerId == 1:
                                self.objdict["tank:0"] = self.othertank
                            else:
                                raise Exception(f"couldn't assign othertank to id; self.playerID = {self.playerId}")
                        else: raise Exception("othertank was none on server connect")
                    case "disconnect":
                        self.connection.offline = True

                    case _:
                        warnings.warn(f"Unknown action received from server: {action}", RuntimeWarning)

        except Exception as error:
            #print("error in handle_connection(): ", error, msg)
            print(self.objdict)
            raise error

    def hit_handler(self, obj, bullet : Bullet):

        #print("hit: ", self, obj, bullet)

        if not self.connection.offline:
            if "hit" not in self.senddict["actions"]:
                self.senddict["actions"].append("hit")
            if "hitinfo" not in self.senddict:
                self.senddict["hitinfo"] = {}

            bulletkey = [key for key, val in self.objdict.items() if val == bullet]
            objkey = [key for key, val in self.objdict.items() if val == obj]

            if len(bulletkey) > 0 and len(objkey) > 0:
                #self.senddict["hitinfo"].append({"hitobject": objkey[0], "bullet": bulletkey[0]})
                self.senddict["hitinfo"]["hitObjectKey"] = objkey[0]
                self.senddict["hitinfo"]["bulletKey"] = bulletkey[0]
            else:
                warnings.warn(f"No key found for object: {obj} or bullet: {bullet}", RuntimeWarning)
        try:
            obj.hit(bullet)
        except:
            warnings.warn(f"error in hit_handler: obj = {obj}; bullet = {bullet}", RuntimeWarning)

        bullet.destroy()
        
    def kill(self):
        self.connection.close()