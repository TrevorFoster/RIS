import math, pygame
from pygame.locals import *
from helpers import Keys, Mouse, Vector2, Constants
from weapons import SingleSquare, SpreadSquare, MachineSquare, ExplosiveSquare, SpinSquare
from managers import projectileManager

class Player:

	def __init__(self, x, y, w, h, colour, speed, health):
		self.pos = Vector2(x, y)
		self.velocity = Vector2()
		self.w = w
		self.h = h
		self.center = [0, 0]
		self.diagLength = math.sqrt(self.w * self.w + self.h * self.h)
		self.angle = 270.0
		self.colour = colour
		self.maxSpeed = speed
		self.speedStep = self.maxSpeed / 50.0
		self.aimerPos = Vector2()
		self.weapon = None
		self.weapons = [SpinSquare(projectileManager, self), SpreadSquare(projectileManager, self), 
						MachineSquare(projectileManager, self), ExplosiveSquare(projectileManager, self)]
		self.selectWeapon(0)
		self.health = health
		self.alive = True
		self.score = 0

	def selectWeapon(self, index):
		if self.weapon:
			self.weapon.stopShooting()

		self.selectedWeapon = index
		self.weapon = self.weapons[index]

	def update(self, camOffset):
		if self.health <= 0:
			self.health = 0
			self.alive = False
			return True
			# n = ""
			# stats[2] += 1
			# self.health = 0
			# self.alive = False
			# for y in range(random.randint(10, 20)):
			#     particles.append(Particle(self.pos.x, self.pos.y, random.uniform(math.radians(0), math.radians(
			#         360)), pv, random.randint(3, 4), (self.colour), random.randint(200, 300)))
		else:
			self.updateSpeed()
			self.updateWeapon()
			self.updateAimer(camOffset)
			return False

	def updateSpeed(self):
		maxedX = abs(self.velocity.x) > self.maxSpeed
		maxedY = abs(self.velocity.y) > self.maxSpeed
		
		diag = False
		if not maxedX and not maxedY:
			# Update player velocity based on keys pressed
			if Keys.pressed(K_w) and Keys.pressed(K_a):
				self.velocity += Vector2(-self.speedStep / Constants.sqrt2, -self.speedStep / Constants.sqrt2)
				diag = True
			elif Keys.pressed(K_w) and Keys.pressed(K_d):
				self.velocity += Vector2(self.speedStep / Constants.sqrt2, -self.speedStep / Constants.sqrt2)
				diag = True
			elif Keys.pressed(K_s) and Keys.pressed(K_a):
				self.velocity += Vector2(-self.speedStep / Constants.sqrt2, self.speedStep / Constants.sqrt2)
				diag = True
			elif Keys.pressed(K_s) and Keys.pressed(K_d):
				self.velocity += Vector2(self.speedStep / Constants.sqrt2, self.speedStep / Constants.sqrt2)
				diag = True

		if not diag and (not maxedX or not maxedY):
			if not maxedY:
				if Keys.pressed(K_w):
					self.velocity += Vector2(0, -self.speedStep)
				elif Keys.pressed(K_s):
					self.velocity += Vector2(0, self.speedStep)
			if not maxedX:
				if Keys.pressed(K_a):
					self.velocity += Vector2(-self.speedStep, 0)
				elif Keys.pressed(K_d):
					self.velocity += Vector2(self.speedStep, 0)

		self.velocity -= self.velocity.normalized() * (self.speedStep / 5.0)
		
		# if velocity is basically 0 velocity = 0
		if abs(self.velocity.x) < 1e-12:
			self.velocity.x = 0
		elif abs(self.velocity.y) < 1e-12:
			self.velocity.y = 0

		self.pos += self.velocity

	def updateWeapon(self):
		for i in range(49, 49 + len(self.weapons)):
			if Keys.get(i).pressedReleased:
				self.selectWeapon(i - 49)
				break

		if Mouse.buttons[0]:
			if not self.weapon.shooting:
				self.weapon.startShooting()
		else:
			self.weapon.stopShooting()

	def updateAimer(self, camOffset):
		mpos = pygame.mouse.get_pos()
		deltax = Mouse.pos.x - (self.pos.x - camOffset.x)
		deltay = Mouse.pos.y - (self.pos.y - camOffset.y)
		self.angle = math.atan2(deltay, deltax)
		
		self.aimerPos = Vector2(math.cos(self.angle) * 20, math.sin(self.angle) * 20)
		offset = Vector2(self.pos.x - 2, self.pos.y - 2)
		self.aimerPos += offset

	def draw(self, screen, camOffset):
		o = pygame.Surface((self.w, self.h))
		o.fill((self.colour))
		o.set_colorkey((0, 0, 0))

		rotated = pygame.transform.rotate(o, math.degrees(self.angle) * -1)
		rotrect = rotated.get_rect()
		self.center = rotrect.center

		screen.blit(rotated, (self.pos.x - rotrect.center[0] - camOffset.x, self.pos.y - rotrect.center[1] - camOffset.y))
		pygame.draw.rect(screen, ((255, 0, 0)), ((
			(self.aimerPos.x) - camOffset.x, (self.aimerPos.y) - camOffset.y), (4, 4)), 1)