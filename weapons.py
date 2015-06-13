import math, random, pygame
from threading import Timer
from helpers import Vector2
from particle import Particle

class Bullet(Particle):

	def __init__(self, x, y, w, h, colour, angle, speed, dps):
		super(Bullet, self).__init__(x, y, w, h, colour, angle, speed)
		self.dps = dps

	def update(self, enemies):
		super(Bullet, self).update()
		rect = pygame.Rect((self.pos.x, self.pos.y), (self.w, self.h))
		for enemy in enemies:
			enemyRect = pygame.Rect(enemy.pos.x, enemy.pos.y, enemy.w, enemy.h)
			if enemyRect.colliderect(rect):
				enemy.hit(self)
				self.destroy()
				return False

		return True


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


class Weapon(object):
	def __init__(self, emitter, owner=None):
		self.owner = owner
		self.shooting = False
		self.timer = None
		self.emitter = emitter

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
	def __init__(self, emitter, owner):
		super(SingleSquare, self).__init__(emitter, owner)
		self.name = "SINGLE SQUARE"
		self.dps = 8
		self.shotInterval = 380
		self.shotSpeed = 6
   
	def shoot(self):
		# midiout.set_instrument(127)
		# midiout.note_on(random.randint(65, 68), 70)
		# stats[0] += 1
		
		self.emitter.add(NormalBullet(self.owner.aimerPos.x - 2, self.owner.aimerPos.y - 2, 9, 9,
		 [random.randint(1, 255) for i in range(3)], self.owner.angle, self.shotSpeed, self.dps))

class SpreadSquare(Weapon):
	def __init__(self, emitter, owner):
		super(SpreadSquare, self).__init__(emitter, owner)
		self.name = "SPREAD SQUARE"
		self.dps = 8
		self.shotInterval = 380
		self.shotSpeed = 6
   
	def shoot(self):
		# midiout.set_instrument(127)
		# midiout.note_on(random.randint(65, 68), 70)
		# stats[0] += 1

		self.emitter.add(NormalBullet(self.owner.aimerPos.x - 2, self.owner.aimerPos.y - 2, 5, 5, [random.randint(1, 255) for i in range(3)], self.owner.angle, self.shotSpeed, self.dps))
		self.emitter.add(NormalBullet(self.owner.aimerPos.x - 2, self.owner.aimerPos.y - 2, 5, 5, [random.randint(1, 255) for i in range(3)], self.owner.angle - math.radians(random.randint(6, 8)), self.shotSpeed, self.dps))
		self.emitter.add(NormalBullet(self.owner.aimerPos.x - 2, self.owner.aimerPos.y - 2, 5, 5, [random.randint(1, 255) for i in range(3)], self.owner.angle + math.radians(random.randint(6, 8)), self.shotSpeed, self.dps))

class MachineSquare(Weapon):
	def __init__(self, emitter, owner):
		super(MachineSquare, self).__init__(emitter, owner)
		self.name = "MACHINE SQUARE"
		self.dps = 1.4
		self.shotInterval = 100
		self.shotSpeed = 6
   
	def shoot(self):
		# midiout.set_instrument(127)
		# midiout.note_on(random.randint(65, 68), 70)
		# stats[0] += 1

		self.emitter.add(NormalBullet(self.owner.aimerPos.x - 2, self.owner.aimerPos.y - 2, 5, 5, 
			[random.randint(1, 255) for i in range(3)], self.owner.angle, self.shotSpeed, self.dps))

class ExplosiveSquare(Weapon):
	def __init__(self, emitter, owner):
		super(ExplosiveSquare, self).__init__(emitter, owner)
		self.name = "EXPLOSIVE SQUARE"
		self.dps = 25.0
		self.shotInterval = 1200
		self.shotSpeed = 6
   
	def shoot(self):
		# midiout.set_instrument(127)
		# midiout.note_on(random.randint(65, 68), 70)
		# stats[0] += 1
		
		self.self.emitter.add(ExplosiveBullet(self.owner.aimerPos.x - 2, self.owner.aimerPos.y - 2, 11, 11, 
			[random.randint(1, 255) for i in range(3)], self.owner.angle, 0, self.dps))

class SpinSquare(Weapon):
	def __init__(self, emitter, owner):
		super(SpinSquare, self).__init__(emitter, owner)
		self.name = "SPIN SQUARE"
		self.dps = 1.4
		self.shotInterval = 50
		self.shotSpeed = 6

	def shoot(self):
		ownerMiddle = Vector2(self.owner.pos.x + self.owner.w / 2, self.owner.pos.y + self.owner.h / 2)
		for i in range(4):
			angle = self.owner.angle + i * (math.pi / 2)
			x = ownerMiddle.x + math.cos(angle) * self.owner.w
			y = ownerMiddle.y + math.sin(angle) * self.owner.h

			self.emitter.add(NormalBullet(x, y, 5, 5, [random.randint(1, 255) for i in range(3)], angle, self.shotSpeed, self.dps))

