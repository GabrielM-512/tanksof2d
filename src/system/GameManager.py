import pygame 
import sys
import math

import warnings

from src.system.ConnectionManager import ConnectionManager
from src.objects.Tank import Tank
from src.objects.Bullet import Bullet

hpfont = pygame.font.SysFont("Arial", 30)

class GameManager:

    UPDATEFREQUENCY = 1
    SCREENLIMIT = 400
    SHOOTINGCOOLDOWN = 2000 # in ms

    def __init__(self, ip: str = "localhost", port : int = "5000", tank_object : Tank = None, other_tank : Tank = None):
        
        self.playerId = None
        self.mode = None

        self.TanksLoadedIn = False

        self.shotbullets = 0

        self.tank = tank_object
        self.tank.callback = self.hit_handler

        self.othertank = other_tank
        self.othertankID = None

        self.old_turret_angle = 0.0

        self.objdict = {
            
        }

        self.senddict = {}

        self.screen = None

        self.offsetScreen = 100

        self.screenscroll = pygame.Vector2(0, 0)
        self.screenscrolldiff = pygame.Vector2(0, 0)

        self.connection = ConnectionManager(host=ip, port=port, callback=self.handle_connection)
        self.playMode = None

        self.points = [0, 0]

        self.hpdisplay = hpfont.render(f"HP: {self.tank.health}", True, (255,255,255))
        self.pdisplay = hpfont.render(f"POINTS {self.points[0]}:{self.points[1]}", True, (255,255,255))
        self.resetdisplay = hpfont.render("You died! Reset with 'R'", True, (255, 255, 255))

        self.bg_texture = pygame.image.load("./assets/background_mud.jpg")

        self.enemy_dir_display_base = pygame.Surface((20, 20))

        self.disconnect = False

        self.has_added_point = False

        try:
            self.connection.connect()
        except Exception as error:
            print(f"Connection to server failed, launching in Singleplayer: {error}")
            self.connection.offline = True
            self.TanksLoadedIn = True


        self.shootcooldown = 0

        self.do_reset = False

    def create_window(self, width, height, description):
        pygame.init()
        screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption(description)
        self.screen = screen
        self.enemy_dir_display_base = pygame.image.load("./assets/enemydir.png").convert_alpha()

    def set_tank_object(self, tank, tank_id):
        self.objdict[f"tank{tank_id}"] = tank

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                self.kill()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if self.tank.maxBullets > len(self.tank.bullets) and self.shootcooldown <= 0:
                        bullet = self.tank.shoot(self.objdict)

                        if bullet is not None:

                            self.shootcooldown = GameManager.SHOOTINGCOOLDOWN

                            self.objdict[f"{self.playerId}:Bullet:{self.shotbullets}"] = bullet

                            if not "shoot" in self.senddict["actions"]:
                                self.senddict["actions"].append("shoot")

                            pos = self.tank.nozzle_position
                            pos[0] += self.screenscroll[0]
                            pos[1] += self.screenscroll[1]

                            self.senddict["shoot"] = {}
                            self.senddict["shoot"]["angle"] = self.tank.turret_angle
                            self.senddict["shoot"]["pos"] = pos # update with screenscroll
                            self.senddict["shoot"]["id"] = f"{self.playerId}:Bullet:{self.shotbullets}"

                            self.shotbullets += 1
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    if self.tank.health <= 0:
                        self.reset(initiate=True)
    
    def update(self, framecount, deltatime):

        for i in range(-2, self.screen.get_width() // self.bg_texture.get_width() + 2):
            for j in range(-2, self.screen.get_height() // self.bg_texture.get_height() + 2):
                self.screen.blit(self.bg_texture, (i * self.bg_texture.get_width() - (self.screenscroll[0] % self.bg_texture.get_width()), j * self.bg_texture.get_height() - (self.screenscroll[1] % self.bg_texture.get_height())))

        if self.screen is None:
            raise Exception("Screen was not defined")

        if self.disconnect:
            self.kill()

        if self.do_reset:
            self.reset()
            self.do_reset = False

        self.shootcooldown -= deltatime
        self.handle_events()
        self.handle_input()

        if self.tank.health <= 0 and self.othertank.health > 0 and not self.has_added_point:
            self.points[1] += 1
            self.has_added_point = True
        elif self.tank.health > 0 and self.othertank.health <= 0 and not self.has_added_point:
            self.points[0] += 1
            self.has_added_point = True

        self.tank.update(self.screen, pygame.Vector2(0, 0), self.screenscrolldiff)
        self.othertank.update(self.screen, self.screenscrolldiff, self.screenscrolldiff)

        if self.tank.health <= 0:
            self.screen.blit(self.resetdisplay, (self.screen.get_width() // 2 - self.resetdisplay.get_width() // 2, 300))

        if self.tank.health <= 0:
            self.hpdisplay = hpfont.render(f"HP: {self.tank.health}", True, (255, 0, 0))
        else:
            self.hpdisplay = hpfont.render(f"HP: {self.tank.health}", True, (255, 255, 255))

        self.pdisplay = hpfont.render(f"POINTS {self.points[0]}:{self.points[1]}", True, (255,255,255))

        self.screen.blit(self.hpdisplay, (20, 20))
        self.screen.blit(self.pdisplay, (20, 60))

        try:
            enemydir = (90 - math.degrees(math.atan2(
                (self.tank.rect.centery + 100) - (self.othertank.rect.centery + 100),  # dy
                (self.tank.rect.centerx + 100) - (self.othertank.rect.centerx + 100)  # dx
            ))) % 360
        except ZeroDivisionError:
            enemydir = 0  # same point

        # if othertank is on screen and both tanks are  alive
        if not (0 <= self.othertank.rect.centerx + 100 <= self.screen.get_width() and 0 <= self.othertank.rect.centery + 100 <= self.screen.get_height()) and self.othertank.health > 0 and self.tank.health > 0:
            enemy_dir_display = pygame.transform.rotate(self.enemy_dir_display_base, enemydir)
            enemydirrect = enemy_dir_display.get_rect()
            enemydirrect.center = (self.screen.get_width() // 2, self.screen.get_height() // 2 - 400)
            self.screen.blit(enemy_dir_display, enemydirrect)

        self.tank.collisions(self.objdict, self.othertankID)

        if framecount % self.UPDATEFREQUENCY == 0 and len(self.senddict['actions']) > 0:
            self.connection.send(self.senddict)
            self.senddict.clear()
            self.senddict["actions"] = []

    def reset(self,initiate = False):
        if (self.tank is not None) or (self.othertank is not None):
            try:
                self.tank.health = 3
                self.othertank.health = 3

                self.screenscroll = pygame.Vector2(0, 0)
                self.screenscrolldiff = pygame.Vector2(0, 0)

                self.has_added_point = False

                self.tank.chassis_angle = 0
                self.othertank.chassis_angle = 0

                self.shootcooldown = 0

                try: 
                    self.objdict["tank:0"].rect.center = (GameManager.SCREENLIMIT + 100, GameManager.SCREENLIMIT + 100)
                    self.objdict["tank:1"].rect.center = (self.screen.get_width() - GameManager.SCREENLIMIT + 100, self.screen.get_height() - GameManager.SCREENLIMIT + 100)
                except Exception as e:
                    print(e, " in reset()")

                # remove the bullets
                try:
                    object_count = 0
                    keys : list = list(self.objdict.keys())

                    while object_count < len(self.objdict):
                        key = keys[object_count]

                        if isinstance(self.objdict[key], Bullet):
                            self.objdict[key].destroy()
                            keys = list(self.objdict.keys())
                        else:
                            object_count += 1

                except Exception as e:
                    print(e, f" in reset(), {initiate}")
                
                if initiate:
                    if not "reset" in self.senddict["actions"]:
                        self.senddict["actions"].append("reset")

            except Exception as error:
                print(f"Error resetting tanks: {error}")
                self.kill()
        else:
            warnings.warn("couldn't reset tank; tank was None", RuntimeWarning)
            self.kill()

    def handle_input(self,) -> None:
        if self.tank is None:
            return

        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.tank.velocity -= self.tank.ACCELERATION
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.tank.velocity += self.tank.ACCELERATION
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.tank.chassis_angle += self.tank.ROTATION_SPEED
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.tank.chassis_angle -= self.tank.ROTATION_SPEED

        if not (keys[pygame.K_w] or keys[pygame.K_s] or keys[pygame.K_UP] or keys[pygame.K_DOWN]):
            if self.tank.velocity > 0:
                if self.tank.velocity > self.tank.DECELERATION:
                    self.tank.velocity -= self.tank.DECELERATION
                else:
                    self.tank.velocity = 0

            if self.tank.velocity < 0:
                if self.tank.velocity < -self.tank.DECELERATION:
                    self.tank.velocity += self.tank.DECELERATION
                else:
                    self.tank.velocity = 0

        if keys[pygame.K_a] or keys[pygame.K_LEFT] or keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            if self.tank.velocity > self.tank.MAX_TURN_SPEED:
                self.tank.velocity -= self.tank.TURN_DECELERATION
            elif self.tank.velocity < -self.tank.MAX_TURN_SPEED:
                self.tank.velocity += self.tank.TURN_DECELERATION

        if self.tank.velocity > self.tank.MAX_SPEED:
            self.tank.velocity = self.tank.MAX_SPEED
        if self.tank.velocity < -self.tank.MAX_SPEED:
            self.tank.velocity = -self.tank.MAX_SPEED

        self.tank.rect.x += self.tank.velocity * math.sin(math.radians(self.tank.chassis_angle))
        self.tank.rect.y += self.tank.velocity * math.cos(math.radians(self.tank.chassis_angle))

        self.screenscrolling()

        if keys[pygame.K_w] or keys[pygame.K_s] or keys[pygame.K_a] or keys[pygame.K_d] or keys[pygame.K_LEFT] or keys[pygame.K_RIGHT] or keys[pygame.K_UP] or keys[pygame.K_DOWN]:
            if not "move" in self.senddict["actions"]:
                self.senddict["actions"].append("move")
            self.senddict["x"] = self.tank.rect.x + self.screenscroll[0]
            self.senddict["y"] = self.tank.rect.y + self.screenscroll[1]

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

    def screenscrolling(self):
        self.screenscrolldiff = pygame.Vector2(0, 0)

        if self.tank.rect.centerx + self.offsetScreen > self.screen.get_width() - GameManager.SCREENLIMIT:
            offsetx = self.tank.rect.centerx + self.offsetScreen - self.screen.get_width() + GameManager.SCREENLIMIT

            self.tank.rect.centerx = self.screen.get_width() - GameManager.SCREENLIMIT - self.offsetScreen

            self.screenscrolldiff[0] = offsetx
            self.screenscroll[0] += offsetx

        elif self.tank.rect.centerx + self.offsetScreen < GameManager.SCREENLIMIT:
            offsetx = (self.tank.rect.centerx + self.offsetScreen) - GameManager.SCREENLIMIT

            self.tank.rect.centerx = GameManager.SCREENLIMIT - self.offsetScreen

            self.screenscrolldiff[0] = offsetx
            self.screenscroll[0] += offsetx

        if self.tank.rect.centery + self.offsetScreen > self.screen.get_height() - GameManager.SCREENLIMIT:
            offsety = self.tank.rect.centery + self.offsetScreen - self.screen.get_height() + GameManager.SCREENLIMIT

            self.tank.rect.centery = self.screen.get_height() - GameManager.SCREENLIMIT - self.offsetScreen

            self.screenscrolldiff[1] = offsety
            self.screenscroll[1] += offsety

        elif self.tank.rect.centery + self.offsetScreen < GameManager.SCREENLIMIT:
            offsety = (self.tank.rect.centery + self.offsetScreen) - GameManager.SCREENLIMIT

            self.tank.rect.centery = GameManager.SCREENLIMIT - self.offsetScreen

            self.screenscrolldiff[1] = offsety
            self.screenscroll[1] += offsety

    def handle_connection(self, msg : dict):
        try:
            actions = msg["actions"]

            for action in actions:
                # noinspection PyUnreachableCode
                match action:
                    case "reset":
                        self.do_reset = True
                    case "move":
                        self.othertank.rect.x = msg["x"] - self.screenscroll[0]
                        self.othertank.rect.y = msg["y"] - self.screenscroll[1]

                    case "turn":
                        self.othertank.chassis_angle = msg["angle"] # seems to lag a little

                    case "turn_turret":
                        self.othertank.turret_angle = msg["turret_angle"]

                    case "shoot": # update
                        old_angle = self.othertank.turret_angle
                        self.othertank.turret_angle = msg["shoot"]["angle"]

                        shootpos = pygame.Vector2(msg["shoot"]["pos"]) - self.screenscroll

                        bullet = self.othertank.shoot(self.objdict, pos=shootpos)

                        if bullet is not None:
                            self.objdict[msg["shoot"]["id"]] = bullet

                        self.othertank.turret_angle = old_angle

                    case "hit":
                        try: 
                            obj = self.objdict[msg["hitinfo"]["hitObjectKey"]]
                            if obj is None:
                                continue

                            bullet : Bullet = self.objdict[msg["hitinfo"]["bulletKey"]]
                            
                            obj.hit(bullet)
                            bullet.destroy()
                        except KeyError:
                            pass
                            #warnings.warn(f"KeyError in hit action: {error}", RuntimeWarning)
                    case "connect":
                        if "actions" not in self.senddict.keys():
                            self.senddict["actions"] = []
                        self.senddict["actions"].append("playerLoadedIn")
                        self.playerId = msg["id"]

                        if self.playerId == 1:
                            self.TanksLoadedIn = True

                        self.playMode = msg["mode"]

                        if self.tank is not None:
                            self.objdict[f"tank:{self.playerId}"] = self.tank
                            self.tank.mode = self.playMode
                        else: raise Exception("tank was none on server connect")

                        if self.othertank is not None:
                            if self.playerId == 0:
                                self.objdict["tank:1"] = self.othertank
                            elif self.playerId == 1:
                                self.objdict["tank:0"] = self.othertank
                            else:
                                raise Exception(f"couldn't assign othertank to id; self.playerID = {self.playerId}")

                            self.othertank.mode = self.playMode
                        else: raise Exception("othertank was none on server connect")
                    case "disconnect":
                        self.disconnect = True
                    case "playerLoadedIn":
                        self.TanksLoadedIn = True
                    case _:
                        warnings.warn(f"Unknown action received from server: {action}", RuntimeWarning)

        except Exception as error:
            print("error in handle_connection(): ", error, msg)
            print(self.objdict)

    def hit_handler(self, obj, bullet : Bullet):
        if not self.connection.offline:
            if "hit" not in self.senddict["actions"]:
                self.senddict["actions"].append("hit")
            if "hitinfo" not in self.senddict:
                self.senddict["hitinfo"] = {}

            bulletkey = [key for key, val in self.objdict.items() if val == bullet]
            objkey = [key for key, val in self.objdict.items() if val == obj]

            if len(bulletkey) > 0 and len(objkey) > 0:
                self.senddict["hitinfo"]["hitObjectKey"] = objkey[0]
                self.senddict["hitinfo"]["bulletKey"] = bulletkey[0]
            else:
                warnings.warn(f"No key found for object: {obj} or bullet: {bullet}", RuntimeWarning)
                print("continued")
        try:
            obj.hit(bullet)
        except Exception as error:
            warnings.warn(f"error: {error} in hit_handler: obj = {obj}; bullet = {bullet}", RuntimeWarning)

        bullet.destroy()
        
    def kill(self):
        self.connection.send({"actions": ["disconnect"]})
        self.connection.close()
        pygame.quit()
        sys.exit()