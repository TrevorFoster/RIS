import math, random, pygame
from helpers import Vector2, Constants
from threading import Timer
from weapons import SpinSquare

class Enemy(object):
	font = None

	def __init__(self, x, y, w, h, health, speed, colour, name):
		self.pos = Vector2(x, y)
		self.w = w
		self.h = h

		self.velocity = Vector2()
		self.health = health
		self.maxSpeed = speed
		self.speedStep = self.maxSpeed / 50.0
		self.facing = 0
		
		self.colour = colour
		self.name = name

		if not Enemy.font:
			Enemy.font = pygame.font.Font("./assets/pixelated.ttf", 15)

	@classmethod
	def random(cls, camOffset, ww, wh):
		xOffs, yOffs = int(camOffset.x), int(camOffset.y)

		spawnPoint = [random.randint(xOffs - 1000, ww + xOffs + 1000), random.randint(yOffs - 1000, wh + yOffs + 1000)]
		enemySpeed = Constants.MAXENEMYSPEED + random.uniform(-.75, .5)
		size = [random.randint(35, 100) for i in range(2)]
		colour = [random.randint(1, 255) for i in range(3)]

		return cls(spawnPoint[0], spawnPoint[1], size[0], size[1], 100, enemySpeed, colour, None)

	def update(self, plyr):
		# Enemy died
		if self.health <= 0:
			self.health = 0

			return False
			# # Play enemy death sound
			# midiout.set_instrument(127)
			# midiout.note_on(random.randint(45, 50), 127)
			# midiout.note_on(random.randint(45, 50), 127)
			# midiout.note_on(random.randint(35, 40), 127)
			# midiout.note_on(random.randint(35, 40), 127)

		deltax = (plyr.pos.x + plyr.w / 2) - (self.pos.x + self.w / 2)
		deltay = (plyr.pos.y + plyr.h / 2) - (self.pos.y + self.h / 2)

		self.facing = math.atan2(deltay, deltax)

		maxedX = abs(self.velocity.x) > self.maxSpeed
		maxedY = abs(self.velocity.y) > self.maxSpeed
		
		if not maxedX:
			self.velocity.x += math.cos(self.facing) * self.speedStep
		if not maxedY:
			self.velocity.y += math.sin(self.facing) * self.speedStep

		self.velocity -= self.velocity.normalized() * (self.speedStep / 5.0)

		# if velocity is basically 0 velocity = 0
		if abs(self.velocity.x) < 1e-12:
			self.velocity.x = 0
		elif abs(self.velocity.y) < 1e-12:
			self.velocity.y = 0

		self.pos += self.velocity

		return True

	def hit(self, projectile):
		self.health -= random.uniform((projectile.dps), (projectile.dps + projectile.dps * 2))
		self.velocity += Vector2(math.cos(projectile.angle), math.sin(projectile.angle)).normalized() * (projectile.speed / 6.0)

		left = random.uniform(.94, .98)
		self.w, self.h = self.w * left, self.h * left

	def collide(self):
		pr = pygame.Rect(plyr.pos.x, plyr.pos.y, plyr.w, plyr.h)
		er = pygame.Rect(self.pos.x, self.pos.y, self.w, self.h)
		if pr.colliderect(er):
			# Player collided with an Enemy
			plyr.health -= random.randint(3, 8)
			midiout.set_instrument(127)
			midiout.note_on(random.randint(60, 65), 80)

			kickx = math.cos(self.facing) * (self.maxSpeed + plyr.speedStep)
			kicky = math.sin(self.facing) * (self.maxSpeed + plyr.speedStep)
			plyr.velocity += Vector2(kickx, kicky)

	def draw(self, screen, camOffset):
		pygame.draw.rect(screen, (self.colour), ((self.pos.x - camOffset.x, self.pos.y - camOffset.y), (self.w, self.h)), 3)
		hp = Enemy.font.render("HP: " + str(math.ceil(self.health)), 5, (self.colour))
		textRect = hp.get_rect(center=(self.pos.x + self.w / 2 - camOffset.x, self.pos.y + self.h + 20 - camOffset.y))
		screen.blit(hp, (textRect[0], textRect[1]))

		if self.name:
			name = Enemy.font.render(str(self.name), 5, (255, 255, 255), (80, 80, 80))
			t = name.get_rect(
				center=(self.x + self.w / 2 - camOffset.x, self.y - 20 - camOffset.y))
			screen.blit(name, (t[0], t[1]))

class Boss(Enemy):
	attackSequence = [
		["follow", 2],
		["spinShoot", 10]
	]

	def __init__(self, x, y, w, h, health, speed, colour, name, emitter):
		super(Boss, self).__init__(x, y, w, h, health, speed, colour, name)
		self.angle = 0
		self.aimerPos = Vector2()
		self.nextAttack = 0
		self.currentAttack = None
		self.currentlyAttacking = False
		self.weapon = None
		self.emitter = emitter

	@classmethod
	def random(cls, camOffset, ww, wh, emitter):
		xOffs, yOffs = int(camOffset.x), int(camOffset.y)

		spawnPoint = [random.randint(xOffs - 1000, ww + xOffs + 1000), random.randint(yOffs - 1000, wh + yOffs + 1000)]
		enemySpeed = Constants.MAXENEMYSPEED + random.uniform(-.75, .5)
		size = [random.randint(100, 150) for i in range(2)]
		colour = [random.randint(1, 255) for i in range(3)]

		return cls(spawnPoint[0], spawnPoint[1], size[0], size[1], 100, enemySpeed, colour, None, emitter)

	def update(self, plyr):
		if self.health <= 0:
			self.health = 0
			if self.weapon:
				self.weapon.stopShooting()
				self.weapon = None
			return False

		if not self.currentlyAttacking:
			self.currentAttack = Boss.attackSequence[self.nextAttack]
			self.currentlyAttacking = True
			attackTimer = Timer(self.currentAttack[1], self.stopAttacking, ())
			attackTimer.start()
		else:
			if self.currentAttack[0] == "follow":
				super(Boss, self).update(plyr)
			elif self.currentAttack[0] == "spinShoot":
				if not self.weapon:
					self.weapon = SpinSquare(self.emitter, self)
					self.weapon.startShooting()
				self.angle += math.pi / 880.0
		return True

	def stopAttacking(self):
		if self.weapon:
			self.weapon.stopShooting()
			self.weapon = None

		self.currentlyAttacking = False
		self.nextAttack += 1
		if self.nextAttack >= len(Boss.attackSequence):
			self.nextAttack = 0

