import random, os, pygame, math
from threading import Timer
from enemy import Enemy, Boss
from particle import Particle
from spaceobjects import Planet, Star

class ResourceManager:
	
	def __init__(self):
		self.resources = {}

	def loadImage(self, path):
		resources = self.resources

		if path in resources:
			return resources[path]
		elif not os.path.isfile(path):
			return None
		else:
			img = pygame.image.load(path).convert_alpha()
			assert img, "Image could not be loaded."

			resources[path] = img
			return img


	def get(self, path):
		return self.resources.get(path)

class EnemyManager:
	
	def __init__(self):
		self.enemies = []
		self.waveNum = 1
		self.wave = None

	def enemyFunc(self, n):
		return 2 * n

	def update(self, plyr, camOffset, ww, wh):
		def updateEnemy(enemy):
			alive = enemy.update(plyr)
			if not alive:
				# Add some particles for enemy explode
				for y in range(random.randint(10, 20)):
					s = random.randint(5, 8)
					particleManager.add(Particle(enemy.pos.x, enemy.pos.y, s, s, (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)), random.uniform(0, math.radians(360)), 1.5))
			
			return alive

		self.enemies = filter(lambda enemy: updateEnemy(enemy), self.enemies)

		if self.wave:
			if self.wave.update(camOffset, ww, wh) and len(self.enemies) == 0:
				self.waveNum += 1
				self.wave = EnemyManager.Wave(self.waveNum, self.enemyFunc(self.waveNum), random.uniform(2.0, 3.0))
		else:
			self.wave = EnemyManager.Wave(self.waveNum, self.enemyFunc(self.waveNum), random.uniform(2.0, 3.0))

	def draw(self, screen, camOffset):
		for enemy in self.enemies:
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
			enemyManager.enemies.append(Enemy.random(camOffset, ww, wh))
			#enemyManager.enemies.append(Boss.random(camOffset, ww, wh, projectileManager))
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

class ParticleManager:

	def __init__(self):
		self.particles = []

	def add(self, particle):
		self.particles.append(particle)

	def update(self):
		for particle in self.particles:
			particle.update()

	def draw(self, screen, camOffset):
		for particle in self.particles:
			particle.draw(screen, camOffset)


class ProjectileManager:
	
	def __init__(self):
		self.projectiles = []	

	def add(self, projectile):
		self.projectiles.append(projectile)

	def update(self):
		self.projectiles = filter(lambda p: p.update(enemyManager.enemies), self.projectiles)
		while len(self.projectiles) > 200:
			self.projectiles.pop(0)

	def draw(self, screen, camOffset):
		for projectile in self.projectiles:
			projectile.draw(screen, camOffset)

class SpaceObjectManager:

	def __init__(self):
		self.planets = []
		self.stars = []

	def load(self):
		images = []
		for i in range(1, 21):
			img = resourceManager.loadImage("./assets/Planet" + str(i) + ".png")
			if img:
				images.append(img)

		for i in range(20):
			self.planets.append(Planet(random.randint(-10000, 10000), random.randint(-10000, 10000),
                           random.randint(-920, -820), images[random.randint(0, len(images) - 1)]))

	def update(self, camOffset, ww, wh):
		for planet in self.planets:
			planet.update(camOffset, ww, wh)
		self.planets.sort(key=lambda planet: planet.z)

		stars = self.stars
		if len(stars) < 50:
			stars.append(Star(random.randint(int(camOffset.x), (ww + int(camOffset.x))), 
	    		random.randint(int(camOffset.y), wh + int(camOffset.y)), 2, 2, (255, 255, 255), 0))
		
		self.stars = filter(lambda star: not star.update(camOffset, ww, wh), stars)

	def draw(self, screen, camOffset):
		for star in self.stars:
			star.draw(screen, camOffset)

		for planet in self.planets:
			planet.draw(screen, camOffset)
		

resourceManager = ResourceManager()
enemyManager = EnemyManager()
particleManager = ParticleManager()
projectileManager = ProjectileManager()
spaceObjectManager = SpaceObjectManager()
