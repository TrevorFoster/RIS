import pygame
from helpers import Vector2, Mouse

class Component(object):
	def __init__(self, x, y, w, h):
		self.pos = Vector2(x, y)
		self.w = w
		self.h = h
		self.inside = False
		self.onClick = []
		self.onMouseEnter = []
		self.onMouseLeave = []
		self.parent = None

	def registerOnClick(self, callback):
		self.onClick.append(callback)
		return callback

	def registerOnMouseEnter(self, callback):
		self.onMouseEnter.append(callback)
		return callback

	def registerOnMouseLeave(self, callback):
		self.onMouseLeave.append(callback)
		return callback

	def align(self):
		if self.parent:
			self.pos.x = self.parent.pos.x + self.parent.w / 2 - self.w / 2

	def update(self):
		buttonRect = pygame.Rect(self.pos.x, self.pos.y, self.w, self.h)
		if buttonRect.collidepoint(Mouse.pos.x, Mouse.pos.y):
			if not self.inside:
				self.inside = True
				for callback in self.onMouseEnter:
					callback()

			if Mouse.buttons[0]:
				for callback in self.onClick:
					callback()
		else:
			if self.inside:
				for callback in self.onMouseLeave:
					callback()
			self.inside = False

	def draw(self, screen):
		pass

class Button(Component):
	def __init__(self, x, y, w, h, text="", colourDict=None):
		super(Button, self).__init__(x, y, w, h)
		self.text = text
		if not colourDict:
			self.colourDict = {
				"base": (0, 0, 0),
				"outline": (255, 255, 255),
				"text": (255, 255, 255)
			}
		else: 
			self.colourDict = colourDict

		@self.registerOnMouseEnter
		def buttonEntered():
			for colour in self.colourDict:
				prevColour = self.colourDict[colour]
				self.colourDict[colour] = (255 - prevColour[0], 255 - prevColour[1], 255 - prevColour[2])

		@self.registerOnMouseLeave
		def buttonLeft():
			for colour in self.colourDict:
				prevColour = self.colourDict[colour]
				self.colourDict[colour] = (255 - prevColour[0], 255 - prevColour[1], 255 - prevColour[2])

	
	def draw(self, screen):
		pygame.draw.rect(screen, self.colourDict["base"], (self.pos.x, self.pos.y, self.w, self.h), 0)
		pygame.draw.rect(screen, self.colourDict["outline"], (self.pos.x, self.pos.y, self.w, self.h), 2)
		
		text = Menu.font.render(self.text, 0, self.colourDict["text"])
		textRect = text.get_rect()
		screen.blit(text, (self.pos.x + self.w/2 - textRect[2] / 2, self.pos.y + self.h / 2 - textRect[3] / 2))

class Image(Component):
	def __init__(self, x, y, w, h, img):
		super(Image, self).__init__(x, y, w, h)
		self.img = img

class Container(Component):
	# align
	# 0 = CENTER
	# layout
	# 0 = VERTICAL
	def __init__(self, x, y, w, h, layout=0, align=0, padding=10):
		super(Container, self).__init__(x, y, w, h)
		self.layout = layout
		self.alignment = align
		self.padding = padding
		self.components = []

	def addComponent(self, component):
		component.parent = self
		self.components.append(component)
		self.align()

	def align(self):
		if self.parent:
			totW, totH = 0, 0

			for i, c in enumerate(self.components):
				totW += c.w
				totH += c.h
				if i < len(self.components) - 1:
					totH += self.padding

			self.w = totW
			self.h = totH

			self.pos.x = self.parent.pos.x + self.parent.w / 2 - totW / 2
			self.pos.y = self.parent.pos.y + self.parent.h / 2 - totH / 2

			cury = self.pos.y
			for i, c in enumerate(self.components):
				c.pos.y = cury
				cury += c.h
				if i < len(self.components) - 1:
					cury += self.padding
		
		for c in self.components:
			c.align()

	def update(self):
		super(Container, self).update()

		for c in self.components:
			c.update()

	def draw(self, screen):
		for c in self.components:
			c.draw(screen)

class View(object):
	def __init__(self):
		self.components = []

	def focus(self):
		self.doLayout()

	def blur(self):
		self.cleanLayout()

	def doLayout(self):
		pass

	def cleanLayout(self):
		self.components = []

	def update(self):
		for c in self.components:
			c.update()

	def draw(self, screen):
		for c in self.components:
			c.draw(screen)

class State:
	def __init__(self, state, view):
		self.state = state
		self.view = view
		self.parent = None

class StateProvider:
	def __init__(self):
		self.currentState = None
		self.states = {}

	def go(self, newState):
		nodes = filter(lambda n: n, newState.split("."))

		if nodes[0] in self.states:
			nextNode = self.states[nodes[0]]
			if newState == nextNode["stateObject"].state:
				self.currentState = nextNode["stateObject"]
				return self.currentState.view

			curNode = nextNode["children"]
		else:
			return None

		for i in range(1, len(nodes)):			
			if nodes[i] not in curNode:
				return None

			nextNode = curNode[nodes[i]]
			if newState == nextNode["stateObject"].state:
				self.currentState = nextNode["stateObject"]
				return self.currentState.view

			curParent = nextNode["stateObject"]
			curNode = nextNode["children"]

		return None

	def state(self, newState):
		nodes = filter(lambda n: n, newState.state.split("."))

		if nodes[0] in self.states:
			curParent = self.states[nodes[0]]["stateObject"]
			curNode = self.states[nodes[0]]["children"]
		else:
			self.states[nodes[0]] = {"stateObject": newState, "children": {}}
			return True

		for i in range(1, len(nodes)):
			if nodes[i] not in curNode:
				newState.parent = curParent
				curNode[nodes[i]] = {"stateObject": newState, "children": {}}
				
				return True

			nextNode = curNode[nodes[i]]
			curParent = nextNode["stateObject"]
			curNode = nextNode["children"]

	def back(self):
		if self.currentState.parent:
			self.currentState = self.currentState.parent
			return self.currentState.view
		return None

class Menu(object):
	stateProvider = StateProvider()
	currentView = None

	def __init__(self):
		self.config()
		Menu.font = pygame.font.Font("./assets/pixelated.ttf", 30)

	def config(self):
		pass

	def draw(self, screen):
		if Menu.currentView:
			Menu.currentView.draw(screen)

	def update(self):
		if Menu.currentView:
			Menu.currentView.update()

	@staticmethod
	def addView(state):
		Menu.stateProvider.state(state)

	@staticmethod
	def focusView(newView):
		if newView:
			if Menu.currentView: Menu.currentView.blur()

			Menu.currentView = newView
			Menu.currentView.focus()

	@staticmethod
	def go(state):
		nextView = Menu.stateProvider.go(state)
		Menu.focusView(nextView)

	@staticmethod
	def back():
		nextView = Menu.stateProvider.back()
		Menu.focusView(nextView)