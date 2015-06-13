import pygame, random

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