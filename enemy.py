import math, random, pygame
from helpers import Vector2, Constants
from threading import Timer
from weapons import Particles, Particle

class Enemies:
	enemies = []
	waveNum = 1
	wave = None

	@staticmethod
	def enemyFunc(n):
		return 2 * n

	@staticmethod
	def spawnRandom(camOffset, ww, wh):
		xOffs, yOffs = int(camOffset.x), int(camOffset.y)

		spawnPoint = [random.randint(xOffs - 1000, ww + xOffs + 1000), random.randint(yOffs - 1000, wh + yOffs + 1000)]
		enemySpeed = Constants.MAXENEMYSPEED + random.uniform(-.75, .5)
		size = [random.randint(35, 100) for i in range(2)]
		colour = [random.randint(1, 255) for i in range(3)]

		Enemies.enemies.append(Enemy(spawnPoint[0], spawnPoint[1], 100, enemySpeed, size[0], size[1], colour, None))

	@staticmethod
	def update(plyr, camOffset, ww, wh):
		Enemies.enemies = filter(lambda enemy: not enemy.update(plyr), Enemies.enemies)

		if Enemies.wave:
			if Enemies.wave.update(camOffset, ww, wh) and len(Enemies.enemies) == 0:
				Enemies.waveNum += 1
				Enemies.wave = Wave(Enemies.waveNum, Enemies.enemyFunc(Enemies.waveNum), random.uniform(2.0, 3.0))
		else:
			Enemies.wave = Wave(Enemies.waveNum, Enemies.enemyFunc(Enemies.waveNum), random.uniform(2.0, 3.0))

	@staticmethod
	def draw(screen, camOffset):
		for enemy in Enemies.enemies:
			enemy.draw(screen, camOffset)

class Wave:
	def __init__(self, wave, spawnTotal, spawnRate):
		self.wave = wave
		self.spawnTotal = spawnTotal
		self.spawnRate = spawnRate
		self.spawned = 0
		self.spawning = False
		self.spawnTimer = None

	def spawn(self, camOffset, ww, wh):
		Enemies.spawnRandom(camOffset, ww, wh)
		self.spawned += 1

	def regulateSpawn(self, camOffset, ww, wh):
		self.spawn(camOffset, ww, wh)
		self.spawning = False
		self.spawnTimer = None

	def update(self, camOffset, ww, wh):
		if self.spawned >= self.spawnTotal: return True
		elif not self.spawning:
			self.spawnTimer = Timer(self.spawnRate, self.regulateSpawn, (camOffset, ww, wh))
			self.spawnTimer.start()
			self.spawning = True
		return False


class Enemy:
	font = None

	def __init__(self, x, y, health, speed, w, h, colour, name):
		self.pos = Vector2(x, y)
		self.velocity = Vector2()

		self.health = health
		self.maxSpeed = speed
		self.speedStep = self.maxSpeed / 50.0
		self.facing = 0
		self.w = w
		self.h = h
		self.colour = colour
		self.name = name

		if not Enemy.font:
			Enemy.font = pygame.font.Font("./assets/pixelated.ttf", 15)

	def update(self, plyr):
		# Enemy died
		if self.health <= 0:
			self.health = 0

			# Add some particles for enemy explode
			for y in range(random.randint(10, 20)):
				s = random.randint(5, 8)
				Particles.add(Particle(self.pos.x, self.pos.y, s, s, (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)), random.uniform(0, math.radians(360)), 1.5))

			return True
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

		return False

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
		hp = Enemy.font.render(
			("HP: " + str(math.ceil(self.health))), 5, (self.colour))
		t = hp.get_rect(center=(self.pos.x + self.w / 2 - camOffset.x, self.pos.y + self.h + 20 - camOffset.y))
		screen.blit(hp, (t[0], t[1]))

		if self.name:
			name = Enemy.font.render(
				str(self.name), 5, (255, 255, 255), (80, 80, 80))
			t = name.get_rect(
				center=(e.x + e.w / 2 - camOffset.x, e.y - 20 - camOffset.y))
			screen.blit(name, (t[0], t[1]))