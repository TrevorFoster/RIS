import random
import time
import math

import sys
import pygame.midi
from game import Game
from helpers import Vector2, Constants, Keys
from weapons import *
try:
    import pygame
except ImportError:
    print"Please install Pygame."
    sys.exit()
from pygame.locals import *


# class Particle:

#     def __init__(self, x, y, angle, speed, s, colour, life):
#         self.x = x
#         self.y = y
#         self.angle = angle
#         self.speed = speed
#         self.s = s
#         self.colour = colour
#         self.life = life

#     def update(self, ww, wh, Or, Ob):
#         self.x += math.cos(self.angle) * self.speed
#         self.y += math.sin(self.angle) * self.speed
#         self.life -= 1
#         if self.x > ww + Or or self.x < 0 + Or or self.y > wh + Ob or self.y < 0 + Ob or self.life <= 0:
#             return True
#         else:
#             return False

#     def draw(self):
#          pygame.draw.rect(
#             screen, (self.colour), ((self.x - outright, self.y - outbottom), (self.w, self.h)), 0
#         )

# class Bullet:

#     def __init__(self, x, y, w, h, dps, colour, angle, speed):
#         self.pos = Vector2(x, y)
#         self.w = w
#         self.h = h
#         self.dps = dps
#         self.colour = colour
#         self.angle = angle
#         self.speed = speed

#     def update(self):
#         self.pos += Vector2(math.cos(self.angle) * self.speed, math.sin(self.angle) * self.speed)

#     def destory(self, particles):
#         pass

#     def draw(self):
#          pygame.draw.rect(
#             screen, (self.colour), ((self.pos.x - outright, self.pos.y - outbottom), (self.w, self.h)), 0
#         )

# class ExplosiveBullet(Bullet):
#     def destroy(self, particles):
#         cols = [(250, 120, 0), (240, 0, 0), (255, 255, 0)]
#         for y in range(random.randint(10, 20)):
#             particles.append(Particle(self.pos.x, self.pos.y, random.uniform(0, math.radians(360)), self.speed, random.randint(
#                 3, 4), cols[random.randint(0, len(cols) - 1)], random.randint(100, 200)))

# class NormalBullet(Bullet):
#     def destroy(self, particles):
#         for y in range(random.randint(1, 2)):
#                 particles.append(Particle(self.pos.x, self.pos.y, random.uniform(angle + math.radians(180), angle + math.radians(360)), self.speed, random.randint(
#                     3, 4), (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)), random.randint(100, 150)))

# class Enemy:

#     def __init__(self, x, y, health, speed, w, h, colour, name):
#         self.pos = Vector2(x, y)
#         self.velocity = Vector2()

#         self.health = health
#         self.maxSpeed = speed
#         self.facing = 0
#         self.w = w
#         self.h = h
#         self.colour = colour
#         self.name = name

#     def update(self):
#         # Enemy died
#         if self.health <= 0:
#             # Play enemy death sound
#             midiout.set_instrument(127)
#             midiout.note_on(random.randint(45, 50), 127)
#             midiout.note_on(random.randint(45, 50), 127)
#             midiout.note_on(random.randint(35, 40), 127)
#             midiout.note_on(random.randint(35, 40), 127)

#             # Add some particles for enemy explode
#             for y in range(random.randint(10, 20)):
#                 Game.particles.append(Particle(self.pos.x, self.pos.y, random.uniform(0, math.radians(360)), pv, random.randint(
#                     5, 8), (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)), random.randint(100, 250)))

#             return True

#         deltax = (plyr.pos.x + plyr.w / 2) - (self.pos.x + self.w / 2)
#         deltay = (plyr.pos.y + plyr.h / 2) - (self.pos.y + self.h / 2)

#         self.facing = math.atan2(deltay, deltax)
#         self.pos.x += math.cos(self.facing) * self.maxSpeed
#         self.pos.y += math.sin(self.facing) * self.maxSpeed

#         return False

#     def hit(self, projectile):
#         self.health -= random.uniform((projectile.dps), (projectile.dps + projectile.dps * 2))

#         left = random.uniform(.94, .98)
#         self.w, self.h = self.w * left, self.h * left

#     def collide(self):
#         pr = pygame.Rect(plyr.pos.x, plyr.pos.y, plyr.w, plyr.h)
#         er = pygame.Rect(self.pos.x, self.pos.y, self.w, self.h)
#         if pr.colliderect(er):
#             # Player collided with an Enemy
#             plyr.health -= random.randint(3, 8)
#             midiout.set_instrument(127)
#             midiout.note_on(random.randint(60, 65), 80)

#             kickx = math.cos(self.facing) * (self.maxSpeed + plyr.speedStep)
#             kicky = math.sin(self.facing) * (self.maxSpeed + plyr.speedStep)
#             plyr.velocity += Vector2(kickx, kicky)

#     def draw(self):
#         pygame.draw.rect(
#             screen, (self.colour), ((self.pos.x - outright, self.pos.y - outbottom), (self.w, self.h)), 3)
#         hp = smallest.render(
#             ("HP: " + str(math.ceil(self.health))), 5, (self.colour))
#         t = hp.get_rect(
#             center=(self.pos.x + self.w / 2 - outright, self.pos.y + self.h + 20 - outbottom))
#         screen.blit(hp, (t[0], t[1]))
#         if self.name != None:
#             name = smallest.render(
#                 str(self.name), 5, (255, 255, 255), (80, 80, 80))
#             t = name.get_rect(
#                 center=(e.x + e.w / 2 - outright, e.y - 20 - outbottom))
#             screen.blit(name, (t[0], t[1]))


# class Player:

#     def __init__(self, x, y, w, h, colour, speed, health):
#         self.pos = Vector2(x, y)
#         self.w = w
#         self.h = h
#         self.velocity = Vector2()
#         self.angle = 270.0
#         self.colour = colour
#         self.maxSpeed = speed
#         self.speedStep = self.maxSpeed / 50.0
#         self.weapon = None
#         self.weapons = [SingleSquare(self), SpreadSquare(self), MachineSquare(self), ExplosiveSquare(self)]
#         self.selectWeapon(0)
#         self.health = health
#         self.alive = True
#         self.score = 0

#     def selectWeapon(self, index):
#         if self.weapon:
#             self.weapon.stopShooting()

#         self.selectedWeapon = index
#         self.weapon = self.weapons[index]

#     def update(self, keys, mouse):
#         global n
#         if self.health <= 0:
#             n = ""
#             stats[2] += 1
#             self.health = 0
#             self.alive = False
#             for y in range(random.randint(10, 20)):
#                 particles.append(Particle(self.pos.x, self.pos.y, random.uniform(math.radians(0), math.radians(
#                     360)), pv, random.randint(3, 4), (self.colour), random.randint(200, 300)))
#         else:
#             self.updateSpeed(keys)
#             self.updateWeapon(keys, mouse)
#             self.updateAimer()

#     def updateSpeed(self, keys):
#         maxedX = abs(self.velocity.x) > self.maxSpeed
#         maxedY = abs(self.velocity.y) > self.maxSpeed
        
#         if not maxedX and not maxedY:
#             # Update player velocity based on keys pressed
#             if keys[K_w] and keys[K_a]:
#                 self.velocity += Vector2(-self.speedStep / Constants.sqrt2, -self.speedStep / Constants.sqrt2)
#             elif keys[K_w] and keys[K_d]:
#                 self.velocity += Vector2(self.speedStep / Constants.sqrt2, -self.speedStep / Constants.sqrt2)
#             elif keys[K_s] and keys[K_a]:
#                 self.velocity += Vector2(-self.speedStep / Constants.sqrt2, self.speedStep / Constants.sqrt2)
#             elif keys[K_s] and keys[K_d]:
#                 self.velocity += Vector2(self.speedStep / Constants.sqrt2, self.speedStep / Constants.sqrt2)
#             else:
#                 if keys[K_w]:
#                     self.velocity += Vector2(0, -self.speedStep)
#                 elif keys[K_s]:
#                     self.velocity += Vector2(0, self.speedStep)
#                 elif keys[K_a]:
#                     self.velocity += Vector2(-self.speedStep, 0)
#                 elif keys[K_d]:
#                     self.velocity += Vector2(self.speedStep, 0)

#         self.velocity -= self.velocity.normalized() * (self.speedStep / 2.0)
        
#         # if velocity is basically 0 velocity = 0
#         if abs(self.velocity.x) < 1e-14:
#             self.velocity.x = 0
#         elif abs(self.velocity.y) < 1e-14:
#             self.velocity.y = 0

#         self.pos += self.velocity

#     def updateWeapon(self, keys, mousestate):
#         for i in range(49, 49 + len(self.weapons)):
#             if Keys.get(i).pressedReleased:
#                 self.selectWeapon(i - 49)
#                 break

#         if mousestate[0]:
#             if not self.weapon.shooting:
#                 self.weapon.startShooting()
#         else:
#             self.weapon.stopShooting()

#     def updateAimer(self):
#         mpos = pygame.mouse.get_pos()
#         deltax = mpos[0] - (self.pos.x - outright)
#         deltay = mpos[1] - (self.pos.y - outbottom)
#         self.angle = math.atan2(deltay, deltax)
        
#         self.aimerPos = Vector2(math.cos(self.angle) * 20, math.sin(self.angle) * 20)
#         offset = Vector2(self.pos.x + self.w / 2 - 2, self.pos.y + self.h / 2 - 2)
#         self.aimerPos += offset

#     def draw(self):
#         global blittedrect
#         o = pygame.Surface((self.w, self.h))
#         ot = pygame.Surface((windw, windh))
#         o.fill((self.colour))
#         ot.fill((0, 0, 0))
#         o.set_colorkey((0, 0, 0))
#         rp = pygame.Rect((0, 0), (self.w, self.h))
#         blittedrect = ot.blit(o, (self.pos.x - outright, self.pos.y - outbottom))
#         oldcenter = blittedrect.center
#         rotated = pygame.transform.rotate(o, math.degrees(angle) * -1)
#         rotrect = rotated.get_rect()
#         rotrect.center = oldcenter
#         screen.blit(rotated, rotrect)
#         pygame.draw.rect(screen, ((255, 0, 0)), ((
#             (self.aimerPos.x) - outright, (self.aimerPos.y) - outbottom), (4, 4)), 1)

# class PlayerMessage:
#     def __init__(self, msg, start, end, time, owner):
#         self.msg = msg
#         self.start = start
#         self.end = end
#         self.owner = owner
#         self.current = Vector2(start.x, start.y)
#         self.frameTimer = None
#         self.frameInterval = self.time / 1000.0
#         self.totalPassed = 0

#     def tick(self):
#         self.totalPassed += self.frameInterval

#     def start(self):
#         self.frameTimer = Timer(self.frameInterval, )


# class Menu:

#     def __init__(self, rects):
#         self.rects = rects
#         self.anim = [
#             [0, 0, False], [0, 0, False], [0, 0, False], [0, 0, False]]
#         self.active = False

#     def update(self, tp, ww, wh, mousestate):
#         run = True
#         paused = True
#         for z in range(len(self.anim)):
#             if False in self.anim[z]:
#                 if self.anim[z][0] >= self.rects[z][1][0] and self.anim[z][1] >= self.rects[z][1][1]:
#                     self.anim[z][2] = True
#                 else:
#                     if self.anim[z][0] <= self.rects[z][1][0]:
#                         if tp > 0:
#                             self.anim[z][
#                                 0] += (self.rects[z][1][0] / ((ww / wh) * 50))
#                     if self.anim[z][1] < self.rects[z][1][1]:
#                         if tp > 0:
#                             self.anim[z][
#                                 1] += (self.rects[z][1][1] / ((ww / wh) * 50))
#             else:
#                 for i in range(len(self.rects)):
#                     b = pygame.Rect((self.rects[i][0][0], self.rects[i][0][
#                                     1]), (self.rects[i][1][0], self.rects[i][1][1]))
#                     if b.collidepoint(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]):
#                         self.rects[i][2] = self.rects[i][4]
#                         if mousestate[0] and str(self.rects[i][5]).upper() == "EXIT GAME":
#                             run = False
#                         if mousestate[0] and str(self.rects[i][5]).upper() == "RESUME GAME":
#                             paused = False
#                             break
#                     else:
#                         self.rects[i][2] = self.rects[i][3]
#         return run, paused


# class Planet:

#     def __init__(self, x, y, z, img):
#         self.x = x
#         self.y = y
#         self.z = z
#         self.zx = 0
#         self.zy = 0
#         self.img = img

#     def update(self, Or, Ob, ww, wh):
#         self.x += .5
#         if self.x >= 10000:
#             self.x = -10000
#             self.y = random.randint(-10000, 10000)
#         self.zx = (self.x - Or - ww / 2) * (self.z / 1000.)
#         self.zy = (self.y - Ob - wh / 2) * (self.z / 1000.)


# class Star:

#     def __init__(self, x, y, w, h, colour, z):
#         self.x = x
#         self.y = y
#         self.w = w
#         self.h = h
#         self.zx = 0
#         self.zy = 0
#         self.colour = colour
#         self.z = z

#     def update(self, Or, Ob, ww, wh):
#         realx = self.x - outright
#         realy = self.y - outbottom

#         if realx < 0.0 or realx > windw or realy < 0.0 or realy > windh:
#             return True
#         else:
#             return False

# def updateplanets():
#     for planet in planets:
#         planet.update(outright, outbottom, windw, windh)
    
#     planets.sort(key=lambda planet: planet.z)

# def updatestars():
#     global stars

#     if len(stars) < 20:
#         boundary = 50
#         stars.append(Star(random.randint(int(outright), windw + int(outright)),
#                           random.randint(int(outbottom), windh + int(outbottom)), 2, 2, (255, 255, 255), 0))

#     stars = filter(lambda star: not star.update(outright, outbottom, windw, windh), stars)

# def updateproj():
#     projectiles = Game.projectiles
#     for projectile in projectiles: projectile.update()

#     if len(projectiles) >= 100:
#         projectiles.pop(0)


# def updatecoins():
#     global coins
#     dlt = []
#     ct = []

#     for x in range(len(coins)):
#         if coins[x][f].collide(pygame.Rect(plyr.pos.x, plyr.pos.y, plyr.w, plyr.h)):
#             dlt.append(x)
#     for x in range(len(coins)):
#         if x not in dlt:
#             ct.append(coins[x])
#     coins = ct


# def updateparticles():
#     Game.particles = filter(lambda particle: not particle.update(windw, windh, outright, outbottom), Game.particles)


# def updateenemies():
#     global enemies
#     def checkEnemy(enemy):
#         if enemy.update():
#             stats[1] += 1
#             return True
#         return False
#     enemies = filter(lambda enemy: not checkEnemy(enemy), enemies)


# def updatemenus(mousestate):
#     running, paused = True, False
#     for i in menus:
#         if i.active:
#             running, paused = i.update(tp, windw, windh, mousestate)
#     return running, paused


# def detecthit():
#     projectiles = Game.projectiles

#     newList = []
#     for p in projectiles:
#         projRect = pygame.Rect((p.pos.x, p.pos.y), (p.w, p.h))
#         collided = False
#         for e in enemies:
#             enemyRect = pygame.Rect(e.pos.x, e.pos.y, e.w, e.h)
#             if enemyRect.colliderect(projRect):
#                 midiout.set_instrument(118)
#                 midiout.note_on(random.randint(95, 100), 112)

#                 e.hit(p)
#                 p.destroy(particles)
#                 collided = True

#         if not collided:
#             newList.append(p)

#     Game.projectiles = newList

# def collide():
#     global enemies
#     for Enemy in enemies:
#         Enemy.collide()

# def drawmenus():
#     global menus
#     for i in menus:
#         if i.active:
#             for x in range(len(i.rects)):
#                 ch = True
#                 if False in i.anim[x]:
#                     ch = False
#                 if ch:
#                     pdisp = menufont.render(
#                         "PAUSED" + "." * (int(tp) / 600) + "", 0, (255, 255, 255))
#                     pr = pdisp.get_rect(center=(windw / 2, windh / 2))
#                     screen.blit(pdisp, (pr[0], 50))
#                     for z in i.rects:
#                         pygame.draw.rect(
#                             screen, (i.rects[x][2]), (i.rects[x][0], i.rects[x][1]), i.rects[x][6])
#                         if i.rects[x][5] != 0:
#                             button = menufont.render(
#                                 i.rects[x][5], 0, (0, 0, 0))
#                             t = button.get_rect(center=(i.rects[x][0][
#                                                 0] + (i.rects[x][1][0] / 2), i.rects[x][0][1] + (i.rects[x][1][1] / 2)))
#                             screen.blit(button, (t[0], t[1]))
#                 else:
#                     pygame.draw.rect(screen, (i.rects[x][2]), (i.rects[x][
#                                      0], (i.anim[x][0], i.anim[x][1])), i.rects[x][6])

pygame.init()
pygame.midi.init()

output_id = pygame.midi.get_default_output_id()
midiout = pygame.midi.Output(1, 0)
midiout.set_instrument(2)
pitches = [24, 26, 28, 29, 31, 33, 35,
           36, 38, 40, 41, 43, 45, 47,
           48, 50, 52, 53, 55, 57, 59,
           60, 62, 64, 65, 67, 69, 71,
           72, 74, 76, 77, 79, 81, 83,
           84, 86, 88, 89, 91, 93, 95]

# statfile = open("./data/stats.txt", "r")
# stats = [int(x) for x in statfile.read().split("\n")]
# statfile.close()
# # Ensure there is initally 4 stats
# if len(stats) < 4: stats.append([0] * (4 - len(stats)))

# scorefile = open("./data/scores.txt", "r")
# scores = map(lambda score: [score[0], int(score[1])], [x.split("|") for x in scorefile.read().split("\n")])
# scorefile.close()

# scores.sort(key=lambda score: score[1])

# bg = pygame.image.load("./assets/background.png").convert_alpha()
# bg = pygame.transform.scale(bg, (windw, windh))
# title = pygame.image.load("./assets/Title.png").convert_alpha()
# menufont = pygame.font.Font("./assets/pixelated.ttf", 30)
# smaller = pygame.font.Font("./assets/pixelated.ttf", 25)
# smallest = pygame.font.Font("./assets/pixelated.ttf", 15)
# ppick = []
# for x in range(1, 21):
#     try:
#         ppick.append(
#             pygame.image.load("./assets/Planet" + str(x) + ".png").convert_alpha())
#     except:
#         pass

# ss = Spritesheet("./assets/Coin.png")

# planets = []
# for x in range(20):
#     planets.append(Planet(random.randint(-10000, 10000), random.randint(-10000, 10000),
#                           random.randint(-920, -820), ppick[random.randint(0, len(ppick) - 1)]))

# clock = pygame.time.Clock()
# pls = windw / windh * 2
# mes = pls / 1.01
# pv = 1.5
# tsl = 0
# tsls = 0.
# tbls = 5000
# pscreen = .2
# tslh = 2000
# mtslc = 2000
# tslc = mtslc
# outright, outbottom = 0, 0

# plyr = Player(windw / 2, windh / 2, 20, 20, (random.randint(1, 255),
#                                              random.randint(1, 255), random.randint(1, 255)), pls, 100)

# animatemenu = [[0, 0, False], [0, 0, False], [0, 0, False], [0, 0, False]]
# menus = [Menu([[[windw / 2 - ((windw / 2) * .4), windh / 2 - ((windh / 2) * .6)], [((windw / 2) * .4) * 2, ((windh / 2) * .6) * 2], [100, 100, 100], [100, 100, 100], [100, 100, 100], 0, 20],
#                [[windw / 2 - ((windw / 2) * .4), windh / 2 - ((windh / 2) * .6)], [((windw / 2) * .4)
#                                                                                    * 2, ((windh / 2) * .6) * 2], [150, 150, 150], [150, 150, 150], [150, 150, 150], 0, 0],
#                [[windw / 2 - ((windw / 2) * .35), (((windh / 2 - ((windh / 2) * .6) + ((windh / 2) * .6) * 2))) - ((windh / 2) * .1) * 4], [
#                    ((windw / 2) * .35) * 2, ((windh / 2) * .1) * 2], [255, 255, 255], [255, 255, 255], [170, 170, 170], "EXIT GAME", 0],
#                [[windw / 2 - ((windw / 2) * .35), (windh / 2 - ((windh / 2) * .6)) + ((windh / 2) * .1) * 2], [((windw / 2) * .35) * 2, ((windh / 2) * .1) * 2], [255, 255, 255], [255, 255, 255], [170, 170, 170], "RESUME GAME", 0]])]
# angle = math.radians(270.)
# weapons = ["SINGLE SQUARE", "SPREAD SQUARE",
#            "MACHINE SQUARE", "EXPLOSIVE SQUARE"]
# n = ""
# cw = 0
# h = 0
# hh = 0
# songf = 0
# f = 0
# paused = False
# running = True
# mainmenu = True
# option, high, stat, score = False, False, False, False
# mute = False
# clicked = False
# full = False
running = True
Game.init()
while running:
    # if not pygame.display.get_active() and not mainmenu and not score:
    #     paused = True
    #     menus[0].active = True
    #     menus[0].anim = [[0, 0, False]for x in range(len(menus[0].rects))]
    #     tp = 0

    running = Game.update()

    Game.draw()

#     keystate = pygame.key.get_pressed()
#     mousestate = pygame.mouse.get_pressed()
#     Keys.update(keystate)
#     for event in pygame.event.get():
#         if score:
#             shift = keystate[K_LSHIFT]
#             if event.type == KEYDOWN:
#                 if event.key in range(97, 123):
#                     if shift:
#                         n += chr(event.key - 32)
#                     else:
#                         n += chr(event.key)
#                 elif event.key == 32:
#                     n += " "
#                 elif event.key == K_BACKSPACE:
#                     n = n[:-1]
#                 if event.key == K_RETURN:
#                     scores.append([n, plyr.score])
#                     scores.sort(key=lambda score: score[1])

#                     mouse = [[1, False]]
#                     score = False
#                     mainmenu = True
#                     n = ""
#                     plyr = Player(windw / 2, windh / 2, 20, 20, (random.randint(1, 255),
#                                                                  random.randint(1, 255), random.randint(1, 255)), pls, 100)
#                     enemies = []
#                     outright, outbottom = 0, 0
#                     cam = Camera(camerarect[0][0], camerarect[0][1], camerarect[1][
#                                  0], camerarect[1][1], windw, windh, outright, outbottom)
#         if event.type == QUIT:
#             running = False

#         if mainmenu:
#             if event.type == MOUSEBUTTONUP and event.button == 1:
#                 clicked = True

#         if event.type == KEYDOWN and not mainmenu and not score:
#             if event.key == K_ESCAPE:
#                 if paused:
#                     paused = False
#                     menus[0].active = False
#                 else:
#                     paused = True
#                     menus[0].active = True
#                     menus[0].anim = [[0, 0, False]
#                                      for x in range(len(menus[0].rects))]
#                     tp = 0

#     if score:
#         if random.randint(1, 100) == 2:  # Fireworks
#             fx, fy = random.randint(
#                 int(outright), windw + int(outright)), random.randint(int(outbottom), windh + int(outbottom))
            
#             midiout.set_instrument(118)
#             midiout.note_on(random.randint(100, 105), 127)
#             midiout.note_on(random.randint(100, 105), 127)
            
#             midiout.set_instrument(127)
#             midiout.note_on(random.randint(35, 40), 127)
#             midiout.note_on(random.randint(35, 40), 127)
            
#             c = (random.randint(2, 255), random.randint(2, 255), random.randint(2, 255))

#             for y in range(random.randint(40, 50)):
#                 particles.append(Particle(fx, fy, random.uniform(
#                     0, math.radians(360)), pv, random.randint(5, 8), c, random.randint(100, 250)))
#     if not paused and not score and not mainmenu:
#         updateplanets()
#         updatestars()
#         updateproj()
#         updateparticles()
#         plyr.update(keystate, mousestate)
#         if not score:
#             if plyr.alive:
#                 detecthit()
#                 if not mainmenu:
#                     outright, outbottom = cam.update()
#                 updatecoins()
#                 if tsls >= tbls:
#                     if len(enemies) < 10 and not mainmenu and not score:
#                         enemies.append(Enemy(random.randint(int(outright) - 1000, windw + int(outright) + 1000), random.randint(int(outbottom) - 1000, windh + int(outbottom) + 1000), 100,
#                                              mes + random.uniform(-.75, .5), random.randint(10, 100), random.randint(10, 100), (random.randint(1, 255), random.randint(1, 255), random.randint(1, 255)), None))
#                     tsls = 0.
#                     tbls = random.randint(1000, 5000)
#                 if not mainmenu:
#                     updateenemies()
#                     collide()

#     else:
#         running, paused = updatemenus(mousestate)

#     if songf >= 380 and not mute:
#         midiout.set_instrument(15)
#         if not paused:
#             note = pitches[random.randint(0, len(pitches) - 1)]
#             midiout.note_on(note, 60)
#             note = pitches[random.randint(0, len(pitches) - 1)]
#             midiout.note_on(note, 60)
#             note = pitches[random.randint(0, len(pitches) - 1)]
#             midiout.note_on(note, 60)
#         else:
#             note = pitches[random.randint(0, len(pitches) - 1)]
#             midiout.note_on(note, 40)
#             note = pitches[random.randint(0, len(pitches) - 1)]
#             midiout.note_on(note, 40)
#             note = pitches[random.randint(0, len(pitches) - 1)]
#             midiout.note_on(note, 40)
#         songf = 0

#     screen.fill((0, 0, 0))
#     drawstars()
#     drawplanets()
#     drawcoins()
#     drawenemies()
#     cam.draw()
#     if plyr.alive and not mainmenu:
#         plyr.draw()
#     drawProjectiles()
#     drawparticles()

#     if tslc > 0 and not mainmenu:
#         wep = smallest.render(weapons[cw], 0, (150, 150, 150))
#         cen = wep.get_rect(center=(blittedrect.center))
#         if plyr.pos.y - h > plyr.pos.y - 40:
#             h += .4
#         screen.blit(wep, (cen[0], plyr.pos.y - h - outbottom))
#     if tslh > 0 and not mainmenu:
#         hel = smallest.render("HP:" + str(plyr.health), 0, (255, 0, 0))
#         cen = hel.get_rect(center=(blittedrect.center))
#         if plyr.pos.y + hh < plyr.pos.y + 40:
#             hh += .4
#         screen.blit(hel, (cen[0], plyr.pos.y + hh - outbottom))
#     if not mainmenu:
#         scr = smaller.render("SCORE:" + str(plyr.score), 0, (255, 255, 0))
#         screen.blit(scr, (0, windh - 30))
#     if mainmenu:
#         screen.blit(title, (windw / 2 - title.get_rect()[2] / 2, 10))
#         srec = pygame.Rect(windw / 2 - 200, windh / 2 - 40, 400, 80)
#         orec = pygame.Rect(windw / 2 - 200, windh / 2 - 40 + 100, 400, 80)
#         erec = pygame.Rect(windw / 2 - 200, windh / 2 - 40 + 200, 400, 80)
#         highrec = pygame.Rect(windw / 2 - 210, windh / 2 - 90, 200, 40)
#         statrec = pygame.Rect(windw / 2 + 10, windh / 2 - 90, 200, 40)
#         if not option and not high and not stat:
#             if not srec.collidepoint(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]):
#                 pygame.draw.rect(
#                     screen, (100, 100, 100), (windw / 2 - 200, windh / 2 - 40, 400, 80))
#                 pygame.draw.rect(
#                     screen, (60, 60, 60), (windw / 2 - 200, windh / 2 - 40, 400, 80), 5)
#             else:
#                 pygame.draw.rect(
#                     screen, (60, 60, 60), (windw / 2 - 200, windh / 2 - 40, 400, 80))
#                 pygame.draw.rect(
#                     screen, (100, 100, 100), (windw / 2 - 200, windh / 2 - 40, 400, 80), 5)
#                 if clicked:
#                     mainmenu = False
#                     stats[3] += 1
#                     plyr = Player(windw / 2, windh / 2, 20, 20, (random.randint(1, 255),
#                                                                  random.randint(1, 255), random.randint(1, 255)), pls, 100)
#             if not orec.collidepoint(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]):
#                 pygame.draw.rect(
#                     screen, (100, 100, 100), (windw / 2 - 200, windh / 2 - 40 + 100, 400, 80))
#                 pygame.draw.rect(
#                     screen, (60, 60, 60), (windw / 2 - 200, windh / 2 - 40 + 100, 400, 80), 5)
#             else:
#                 pygame.draw.rect(
#                     screen, (60, 60, 60), (windw / 2 - 200, windh / 2 - 40 + 100, 400, 80))
#                 pygame.draw.rect(
#                     screen, (100, 100, 100), (windw / 2 - 200, windh / 2 - 40 + 100, 400, 80), 5)
#                 if clicked:
#                     option = True
#             if not erec.collidepoint(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]):
#                 pygame.draw.rect(
#                     screen, (100, 100, 100), (windw / 2 - 200, windh / 2 - 40 + 200, 400, 80))
#                 pygame.draw.rect(
#                     screen, (60, 60, 60), (windw / 2 - 200, windh / 2 - 40 + 200, 400, 80), 5)
#             else:
#                 pygame.draw.rect(
#                     screen, (60, 60, 60), (windw / 2 - 200, windh / 2 - 40 + 200, 400, 80))
#                 pygame.draw.rect(
#                     screen, (100, 100, 100), (windw / 2 - 200, windh / 2 - 40 + 200, 400, 80), 5)
#                 if clicked:
#                     running = False
#             if not highrec.collidepoint(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]):
#                 pygame.draw.rect(
#                     screen, (100, 100, 100), (windw / 2 - 210, windh / 2 - 90, 200, 40))
#                 pygame.draw.rect(
#                     screen, (60, 60, 60), (windw / 2 - 210, windh / 2 - 90, 200, 40), 5)
#             else:
#                 pygame.draw.rect(
#                     screen, (60, 60, 60), (windw / 2 - 210, windh / 2 - 90, 200, 40))
#                 pygame.draw.rect(
#                     screen, (100, 100, 100), (windw / 2 - 210, windh / 2 - 90, 200, 40), 5)
#                 if clicked:
#                     high = True

#             if not statrec.collidepoint(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]):
#                 pygame.draw.rect(
#                     screen, (100, 100, 100), (windw / 2 + 10, windh / 2 - 90, 200, 40))
#                 pygame.draw.rect(
#                     screen, (60, 60, 60), (windw / 2 + 10, windh / 2 - 90, 200, 40), 5)
#             else:
#                 pygame.draw.rect(
#                     screen, (60, 60, 60), (windw / 2 + 10, windh / 2 - 90, 200, 40))
#                 pygame.draw.rect(
#                     screen, (100, 100, 100), (windw / 2 + 10, windh / 2 - 90, 200, 40), 5)
#                 if clicked:
#                     stat = True
#             clicked = False
#         elif option:
#             if not srec.collidepoint(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]):
#                 pygame.draw.rect(
#                     screen, (100, 100, 100), (windw / 2 - 200, windh / 2 - 40, 400, 80))
#                 pygame.draw.rect(
#                     screen, (60, 60, 60), (windw / 2 - 200, windh / 2 - 40, 400, 80), 5)
#             else:
#                 pygame.draw.rect(
#                     screen, (60, 60, 60), (windw / 2 - 200, windh / 2 - 40, 400, 80))
#                 pygame.draw.rect(
#                     screen, (100, 100, 100), (windw / 2 - 200, windh / 2 - 40, 400, 80), 5)
#                 if clicked:
#                     if windw != maxres[0]:
#                         full = True
#                         windw, windh = maxres[0], maxres[1]
#                         screen = pygame.display.set_mode((windw, windh), pygame.FULLSCREEN, 32)
#                     else:
#                         full = False
#                         windw, windh = 800, 600
#                         screen = pygame.display.set_mode((windw, windh), 0, 32)
#                     menus = [Menu([[[windw / 2 - ((windw / 2) * .4), windh / 2 - ((windh / 2) * .6)], [((windw / 2) * .4) * 2, ((windh / 2) * .6) * 2], [100, 100, 100], [100, 100, 100], [100, 100, 100], 0, 20],
#                                    [[windw / 2 - ((windw / 2) * .4), windh / 2 - ((windh / 2) * .6)], [((windw / 2) * .4) * 2, ((
#                                        windh / 2) * .6) * 2], [150, 150, 150], [150, 150, 150], [150, 150, 150], 0, 0],
#                                    [[windw / 2 - ((windw / 2) * .35), (((windh / 2 - ((windh / 2) * .6) + ((windh / 2) * .6) * 2))) - ((windh / 2) * .1) * 4], [
#                                        ((windw / 2) * .35) * 2, ((windh / 2) * .1) * 2], [255, 255, 255], [255, 255, 255], [170, 170, 170], "EXIT GAME", 0],
#                                    [[windw / 2 - ((windw / 2) * .35), (windh / 2 - ((windh / 2) * .6)) + ((windh / 2) * .1) * 2], [((windw / 2) * .35) * 2, ((windh / 2) * .1) * 2], [255, 255, 255], [255, 255, 255], [170, 170, 170], "RESUME GAME", 0]])]
#                     bg = pygame.transform.scale(bg, (windw, windh))
#                     camerarect = [[(windw / 2 - ((windw / 2) * pscreen)), (windh / 2 - (
#                         (windh / 2) * pscreen))], [((windw / 2) * pscreen) * 2, ((windh / 2) * pscreen) * 2]]
#                     cam = Camera(camerarect[0][0], camerarect[0][1], camerarect[1][
#                                  0], camerarect[1][1], windw, windh, outright, outbottom)
#             if not orec.collidepoint(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]):
#                 pygame.draw.rect(
#                     screen, (100, 100, 100), (windw / 2 - 200, windh / 2 - 40 + 100, 400, 80))
#                 pygame.draw.rect(
#                     screen, (60, 60, 60), (windw / 2 - 200, windh / 2 - 40 + 100, 400, 80), 5)
#             else:
#                 pygame.draw.rect(
#                     screen, (60, 60, 60), (windw / 2 - 200, windh / 2 - 40 + 100, 400, 80))
#                 pygame.draw.rect(
#                     screen, (100, 100, 100), (windw / 2 - 200, windh / 2 - 40 + 100, 400, 80), 5)
#                 if clicked:
#                     if mute:
#                         mute = False
#                     else:
#                         mute = True
#             if not erec.collidepoint(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]):
#                 pygame.draw.rect(
#                     screen, (100, 100, 100), (windw / 2 - 200, windh / 2 - 40 + 200, 400, 80))
#                 pygame.draw.rect(
#                     screen, (60, 60, 60), (windw / 2 - 200, windh / 2 - 40 + 200, 400, 80), 5)
#             else:
#                 pygame.draw.rect(
#                     screen, (60, 60, 60), (windw / 2 - 200, windh / 2 - 40 + 200, 400, 80))
#                 pygame.draw.rect(
#                     screen, (100, 100, 100), (windw / 2 - 200, windh / 2 - 40 + 200, 400, 80), 5)
#                 if clicked:
#                     option = False
#             clicked = False
#         elif high:
#             if not erec.collidepoint(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]):
#                 pygame.draw.rect(
#                     screen, (100, 100, 100), (windw / 2 - 200, windh / 2 - 40 + 200, 400, 80))
#                 pygame.draw.rect(
#                     screen, (60, 60, 60), (windw / 2 - 200, windh / 2 - 40 + 200, 400, 80), 5)
#             else:
#                 pygame.draw.rect(
#                     screen, (60, 60, 60), (windw / 2 - 200, windh / 2 - 40 + 200, 400, 80))
#                 pygame.draw.rect(
#                     screen, (100, 100, 100), (windw / 2 - 200, windh / 2 - 40 + 200, 400, 80), 5)
#                 if clicked:
#                     high = False
#             clicked = False
#         elif stat:
#             if not orec.collidepoint(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]):
#                 pygame.draw.rect(
#                     screen, (100, 100, 100), (windw / 2 - 200, windh / 2 - 40 + 100, 400, 80))
#                 pygame.draw.rect(
#                     screen, (60, 60, 60), (windw / 2 - 200, windh / 2 - 40 + 100, 400, 80), 5)
#             else:
#                 pygame.draw.rect(
#                     screen, (60, 60, 60), (windw / 2 - 200, windh / 2 - 40 + 100, 400, 80))
#                 pygame.draw.rect(
#                     screen, (100, 100, 100), (windw / 2 - 200, windh / 2 - 40 + 100, 400, 80), 5)
#                 if clicked:
#                     stat = False
#             clicked = False
#         if not option and not high and not stat:
#             play = menufont.render("PLAY!", 0, (255, 255, 255))
#             options = menufont.render("OPTIONS", 0, (255, 255, 255))
#             exitg = menufont.render("EXIT GAME", 0, (255, 255, 255))
#             highscore = smaller.render("HIGHSCORES", 0, (255, 255, 255))
#             statss = smaller.render("STATS", 0, (255, 255, 255))
#             screen.blit(
#                 play, (windw / 2 - play.get_rect()[2] / 2, windh / 2 - play.get_rect()[3] / 2))
#             screen.blit(options, (windw / 2 - options.get_rect()
#                                   [2] / 2, windh / 2 - options.get_rect()[3] / 2 + 100))
#             screen.blit(exitg, (windw / 2 - exitg.get_rect()
#                                 [2] / 2, windh / 2 - exitg.get_rect()[3] / 2 + 200))
#             screen.blit(highscore, (windw / 2 - 204, windh / 2 - 85))
#             screen.blit(statss, (windw / 2 + 60, windh / 2 - 85))
#         elif option:
#             toggle = menufont.render("TOGGLE FULLSCREEN", 0, (255, 255, 255))
#             mu = menufont.render(
#                 "MUTE MUSIC: " + str(mute), 0, (255, 255, 255))
#             back = menufont.render("BACK", 0, (255, 255, 255))
#             screen.blit(toggle, (windw / 2 - toggle.get_rect()
#                                  [2] / 2, windh / 2 - toggle.get_rect()[3] / 2))
#             screen.blit(
#                 mu, (windw / 2 - mu.get_rect()[2] / 2, windh / 2 - mu.get_rect()[3] / 2 + 100))
#             screen.blit(back, (windw / 2 - back.get_rect()
#                                [2] / 2, windh / 2 - back.get_rect()[3] / 2 + 200))
#         elif high:
#             back = menufont.render("BACK", 0, (255, 255, 255))
#             players = []
#             c = 0
#             for i in scores:
#                 if full:
#                     if c < 15:
#                         players.append(menufont.render(
#                             str(c + 1) + ". " + i[0] + " - " + str(i[1]), 0, (255, 255, 255)))
#                 else:
#                     if c < 8:
#                         players.append(menufont.render(
#                             str(c + 1) + ". " + i[0] + " - " + str(i[1]), 0, (255, 255, 255)))
#                 c += 1
#             back = menufont.render("BACK", 0, (255, 255, 255))
#             screen.blit(back, (windw / 2 - back.get_rect()
#                                [2] / 2, windh / 2 - back.get_rect()[3] / 2 + 200))
#             for i in range(len(players)):
#                 screen.blit(
#                     players[i], (windw / 2 - players[i].get_rect()[2] / 2, i * 30 + 200))
#         elif stat:
#             fired = menufont.render(
#                 "SHOTS FIRED - " + str(stats[0]), 0, (255, 255, 255))
#             killed = menufont.render(
#                 "ENEMIES KILLED - " + str(stats[1]), 0, (255, 255, 255))
#             deaths = menufont.render(
#                 "DEATHS - " + str(stats[2]), 0, (255, 255, 255))
#             plays = menufont.render(
#                 "TIMES PLAYED - " + str(stats[3]), 0, (255, 255, 255))
#             back = menufont.render("BACK", 0, (255, 255, 255))
#             screen.blit(back, (windw / 2 - back.get_rect()
#                                [2] / 2, windh / 2 - back.get_rect()[3] / 2 + 100))
#             screen.blit(
#                 fired, (windw / 2 - fired.get_rect()[2] / 2, windh / 2 - 110))
#             screen.blit(
#                 killed, (windw / 2 - killed.get_rect()[2] / 2, windh / 2 - 70))
#             screen.blit(
#                 deaths, (windw / 2 - deaths.get_rect()[2] / 2, windh / 2 - 30))
#             screen.blit(
#                 plays, (windw / 2 - plays.get_rect()[2] / 2, windh / 2 + 10))
#     if score:
#         over = menufont.render("GAME OVER", 0, (255, 255, 255))
#         name = menufont.render("ENTER YOUR NAME: " + n, 0, (255, 255, 255))
#         scoredisp = menufont.render(
#             "SCORE: " + str(plyr.score), 0, (255, 255, 255))
#         screen.blit(over, (windw / 2 - over.get_rect()[2] / 2, windh / 2 - 60))
#         screen.blit(name, (windw / 2 - name.get_rect()[2] / 2, windh / 2))
#         screen.blit(
#             scoredisp, (windw / 2 - scoredisp.get_rect()[2] / 2, windh / 2 + 60))
#     if paused:
#         screen.blit(bg, (0, 0))
#         if tp >= 2000:
#             tp = 0.
#         else:
#             tp += mili
#         drawmenus()
#     pygame.display.update(pygame.Rect(0, 0, windw, windh))
#     mili = clock.tick(200)
#     print mili
#     tsl += mili
#     tsls += mili
#     tslh -= mili
#     tslc -= mili
#     if not mute:
#         songf += mili
# pygame.quit()
# pygame.midi.quit()

# statfile = open("./data/stats.txt", "w")
# for x in range(len(stats)):
#     if x < len(stats) - 1:
#         statfile.write(str(stats[x]) + "\n")
#     else:
#         statfile.write(str(stats[x]))
# statfile.close()

# scorefile = open("./data/scores.txt", "w")
# for x in range(len(scores)):
#     if x < len(scores) - 1:
#         scorefile.write(scores[x][0] + "|" + str(scores[x][1]) + "\n")
#     else:
#         scorefile.write(scores[x][0] + "|" + str(scores[x][1]))
# scorefile.close()
