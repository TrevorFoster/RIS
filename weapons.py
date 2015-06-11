import math, random, pygame
from threading import Timer
from helpers import Vector2

class Particle(object):

	def __init__(self, x, y, w, h, colour, angle, speed):
		self.pos = Vector2(x, y)
		self.w = w
		self.h = h
		self.colour = colour
		self.angle = angle
		self.speed = speed

	def update(self):
		self.pos += Vector2(math.cos(self.angle) * self.speed, math.sin(self.angle) * self.speed)

	def draw(self, screen, camOffset):
		 pygame.draw.rect(
			screen, self.colour, ((self.pos.x - camOffset.x, self.pos.y - camOffset.y), (self.w, self.h)), 0)

class Bullet(Particle):

	def __init__(self, x, y, w, h, colour, angle, speed, dps):
		super(Bullet, self).__init__(x, y, w, h, colour, angle, speed)
		self.dps = dps

	# Abstract method overridden by different types of bullets
	def destory(self):
		pass

class ExplosiveBullet(Bullet):
	def destroy(self):
		cols = [(250, 120, 0), (240, 0, 0), (255, 255, 0)]
		# for y in range(random.randint(10, 20)):
		#     particles.append(Particle(self.pos.x, self.pos.y, random.uniform(0, math.radians(360)), self.speed, random.randint(
		#         3, 4), cols[random.randint(0, len(cols) - 1)], random.randint(100, 200)))

class NormalBullet(Bullet):
	def destroy(self): pass
		# for y in range(random.randint(1, 2)):
		#         particles.append(Particle(self.pos.x, self.pos.y, random.uniform(angle + math.radians(180), angle + math.radians(360)), self.speed, random.randint(
		#             3, 4), (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)), random.randint(100, 150)))

class Particles:
	particles = []

	@staticmethod
	def add(particle):
		Particles.particles.append(particle)

	@staticmethod
	def update():
		for particle in Particles.particles:
			particle.update()

	@staticmethod
	def draw(screen, camOffset):
		for particle in Particles.particles:
			particle.draw(screen, camOffset)


class Projectiles:
	projectiles = []

	@staticmethod
	def add(projectile):
		Projectiles.projectiles.append(projectile)

	@staticmethod
	def update(enemies):
		for projectile in Projectiles.projectiles:
			projectile.update()

		newList = []
		for projectile in Projectiles.projectiles:
			projRect = pygame.Rect((projectile.pos.x, projectile.pos.y), (projectile.w, projectile.h))
			collided = False
			for enemy in enemies:
				enemyRect = pygame.Rect(enemy.pos.x, enemy.pos.y, enemy.w, enemy.h)
				if enemyRect.colliderect(projRect):
					# midiout.set_instrument(118)
					# midiout.note_on(random.randint(95, 100), 112)

					enemy.hit(projectile)
					projectile.destroy()
					collided = True

			if not collided:
				newList.append(projectile)

		Projectiles.projectiles = newList

	@staticmethod
	def draw(screen, camOffset):
		for projectile in Projectiles.projectiles:
			projectile.draw(screen, camOffset)


class Weapon(object):
	def __init__(self, owner=None):
		self.owner = owner
		self.shooting = False
		self.timer = None

	def regulateShooting(self):
		self.shoot()
		if self.shooting:
			self.timer = Timer(self.shotInterval / 1000.0, self.regulateShooting, ())
			self.timer.start()

	def startShooting(self):
		if not self.shooting:
			self.shooting = True
			self.shoot()
			self.timer = Timer(self.shotInterval / 1000.0, self.regulateShooting, ())
			self.timer.start()

	def stopShooting(self):
		if self.timer != None:
			self.shooting = False
			self.timer.cancel()

	def shoot(self):
		pass

class SingleSquare(Weapon):
	def __init__(self, owner):
		super(SingleSquare, self).__init__(owner)
		self.name = "SINGLE SQUARE"
		self.dps = 8
		self.shotInterval = 380
		self.shotSpeed = 6
   
	def shoot(self):
		# midiout.set_instrument(127)
		# midiout.note_on(random.randint(65, 68), 70)
		# stats[0] += 1
		
		Projectiles.add(NormalBullet(self.owner.aimerPos.x - 2, self.owner.aimerPos.y - 2, 9, 9,
		 (random.randint(1, 255), random.randint(1, 255), random.randint(1, 255)), self.owner.angle, self.shotSpeed, self.dps))

class SpreadSquare(Weapon):
	def __init__(self, owner):
		super(SpreadSquare, self).__init__(owner)
		self.name = "SPREAD SQUARE"
		self.dps = 8
		self.shotInterval = 380
		self.shotSpeed = 6
   
	def shoot(self):
		# midiout.set_instrument(127)
		# midiout.note_on(random.randint(65, 68), 70)
		# stats[0] += 1

		Projectiles.add(NormalBullet(self.owner.aimerPos.x - 2, self.owner.aimerPos.y - 2, 5, 5, 
			(random.randint(1, 255), random.randint(1, 255), random.randint(1, 255)), self.owner.angle, self.shotSpeed, self.dps))
		Projectiles.add(NormalBullet(self.owner.aimerPos.x - 2, self.owner.aimerPos.y - 2, 5, 5, (random.randint(1, 255), 
			random.randint(1, 255), random.randint(1, 255)), self.owner.angle - math.radians(random.randint(6, 8)), self.shotSpeed, self.dps))
		Projectiles.add(NormalBullet(self.owner.aimerPos.x - 2, self.owner.aimerPos.y - 2, 5, 5, (random.randint(1, 255), 
			random.randint(1, 255), random.randint(1, 255)), self.owner.angle + math.radians(random.randint(6, 8)), self.shotSpeed, self.dps))

class MachineSquare(Weapon):
	def __init__(self, owner):
		super(MachineSquare, self).__init__(owner)
		self.name = "MACHINE SQUARE"
		self.dps = 1.4
		self.shotInterval = 100
		self.shotSpeed = 6
   
	def shoot(self):
		# midiout.set_instrument(127)
		# midiout.note_on(random.randint(65, 68), 70)
		# stats[0] += 1

		Projectiles.add(NormalBullet(self.owner.aimerPos.x - 2, self.owner.aimerPos.y - 2, 5, 5, 
			(random.randint(1, 255), random.randint(1, 255), random.randint(1, 255)), self.owner.angle, self.shotSpeed, self.dps))

class ExplosiveSquare(Weapon):
	def __init__(self, owner):
		super(ExplosiveSquare, self).__init__(owner)
		self.name = "EXPLOSIVE SQUARE"
		self.dps = 25.0
		self.shotInterval = 1200
		self.shotSpeed = 6
   
	def shoot(self):
		# midiout.set_instrument(127)
		# midiout.note_on(random.randint(65, 68), 70)
		# stats[0] += 1
		
		Projectiles.add(ExplosiveBullet(self.owner.aimerPos.x - 2, self.owner.aimerPos.y - 2, 11, 11, 
			(random.randint(1, 255), random.randint(1, 255), random.randint(1, 255)), self.owner.angle, 0, self.dps))