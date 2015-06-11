import pygame, random
from resources import ResourceManager

class SpaceObjects:
	planets = []
	stars = []

	@staticmethod
	def load():
		images = []
		for i in range(1, 21):
			img = ResourceManager.loadImage("./assets/Planet" + str(i) + ".png")
			if img:
				images.append(img)

		for i in range(20):
			SpaceObjects.planets.append(Planet(random.randint(-10000, 10000), random.randint(-10000, 10000),
                           random.randint(-920, -820), images[random.randint(0, len(images) - 1)]))

	@staticmethod
	def update(camOffset, ww, wh):
		for planet in SpaceObjects.planets:
			planet.update(camOffset, ww, wh)
		SpaceObjects.planets.sort(key=lambda planet: planet.z)

		stars = SpaceObjects.stars
		if len(stars) < 50:
			stars.append(Star(random.randint(int(camOffset.x), (ww + int(camOffset.x))), 
	    		random.randint(int(camOffset.y), wh + int(camOffset.y)), 2, 2, (255, 255, 255), 0))
		
		SpaceObjects.stars = filter(lambda star: not star.update(camOffset, ww, wh), stars)

	@staticmethod
	def draw(screen, camOffset):
		for planet in SpaceObjects.planets:
			planet.draw(screen, camOffset)

		for star in SpaceObjects.stars:
			star.draw(screen, camOffset)


class Planet:

    def __init__(self, x, y, z, img):
        self.x = x
        self.y = y
        self.z = z
        self.zx = 0
        self.zy = 0
        self.img = img

    def update(self, camOffset, ww, wh):
        self.x += .5
        if self.x >= 10000:
            self.x = -10000
            self.y = random.randint(-10000, 10000)
        self.zx = (self.x - camOffset.x - ww / 2) * (self.z / 1000.)
        self.zy = (self.y - camOffset.y - wh / 2) * (self.z / 1000.)

    def draw(self, screen, camOffset):
    	#if self.x - camOffset.x + self.zx < ww and (self.x + self.img.get_rect()[2]) - camOffset.x + self.zx > 0 and self.y - camOffset.y + self.zy < wh and (self.y + self.img.get_rect()[3]) - camOffset.y + self.zy > 0:
        screen.blit(self.img, (self.x - camOffset.x + self.zx, self.y - camOffset.y + self.zy))


class Star:

    def __init__(self, x, y, w, h, colour, z):
        self.x = x
        self.y = y
        self.z = z
        self.w = w
        self.h = h
        self.zx = 0
        self.zy = 0
        self.colour = colour

    def update(self, camOffset, ww, wh):
    	realx, realy = self.x - camOffset.x, self.y - camOffset.y

    	self.zx = (realx - ww / 2) * (self.z / 1000.)
        self.zy = (realy - wh / 2) * (self.z / 1000.)

        if realx < 0.0 or realx > ww or realy < 0.0 or realy > wh:
            return True
        else:
            return False

    def draw(self, screen, camOffset):
    	pygame.draw.rect(
                screen, self.colour, (self.x - camOffset.x + self.zx, self.y - camOffset.y + self.zy, self.w, self.h))