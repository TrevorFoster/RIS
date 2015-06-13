import pygame, math
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