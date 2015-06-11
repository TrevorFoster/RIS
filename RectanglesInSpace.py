try:
	import pygame
except ImportError:
	import sys
	print "Please install Pygame."
	sys.exit()

import pygame.midi
from pygame.locals import *

import random, math
from game import Game
from helpers import Vector2, Constants
from weapons import *

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

clock = pygame.time.Clock()
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
	mili = clock.tick(200)

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
	
#     print mili
#     tsl += mili
#     tsls += mili
#     tslh -= mili
#     tslc -= mili
#     if not mute:
#         songf += mili
pygame.midi.quit()
pygame.quit()


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
