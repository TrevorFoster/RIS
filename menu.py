import pygame
from helpers import Vector2, Mouse
from managers import resourceManager

class Event:
	def __init__(self, name):
		self.name = name
		self._callbacks = []

	def trigger(self):
		for callback in self._callbacks:
			callback[0](self, callback[1])

	def register(self, callback, *args):
		self._callbacks.append([callback, args])
		return callback

class GameTimer:
	timers = []
	def __init__(self, time, event):
		self.time = time
		self.event = event
		self.passed = 0.0
		GameTimer.timers.append(self)

	def update(self, millis):
		self.passed += millis
		if self.passed >= self.time:
			self.event.trigger()
			self.passed = 0.0
			return True
		return False

	@staticmethod
	def unregister(timer):
		for i, t in enumerate(GameTimer.timers):
			if t == timer:
				GameTimer.pop(i)
				return True

		return False

	@staticmethod
	def tick(millis):
		for timer in GameTimer.timers:
			timer.update(millis)


class Component(object):
	defaults = {
		"width": 10,
		"height": 10,
		"position": Vector2(),
		"horizontal_align": 0,
		"colour": (0, 0, 0),
		"background_colour": None,
		"border_colour": None,
		"layout": 0,
		"padding": 0,
		"hover": {}
	}

	def __init__(self, **args):
		self.attr = args
		self.parseAttr()

		self.pos = Vector2()
		self.inside = False
		self.parent = None
		self.overridden = {}

		self.onClick = Event("onClick")
		self.onMouseEnter = Event("onMouseEnter")
		self.onMouseLeave = Event("onMouseLeave")
		
		self.onMouseEnter.register(self.mouseEnter)
		self.onMouseLeave.register(self.mouseLeave)

	def parseAttr(self):
		for attr, value in Component.defaults.iteritems():
			self.attr.setdefault(attr, value)

		self.pos = self.attr["position"]
		self.w = self.attr["width"]
		self.h = self.attr["height"]

	def align(self):
		if self.parent:
			horAlign = self.attr["horizontal_align"]
			if horAlign == 0:
				self.pos.x = self.parent.pos.x + self.parent.w / 2 - self.w / 2
			elif horAlign == 1:
				self.pos.x = self.parent.pos.x

	def update(self):
		buttonRect = pygame.Rect(self.pos.x, self.pos.y, self.w, self.h)
		if buttonRect.collidepoint(Mouse.pos.x, Mouse.pos.y):
			if not self.inside:
				self.inside = True
				self.onMouseEnter.trigger()

			if Mouse.leftClicked:
				self.onClick.trigger()
		else:
			if self.inside:
				self.onMouseLeave.trigger()
			self.inside = False

	def mouseEnter(self, e, args):
		self.overridden = {}
		for attr, value in self.attr["hover"].iteritems():
			self.overridden[attr] = self.attr[attr]
			self.attr[attr] = value

		if "width" in self.overridden:
			self.w = self.attr["width"]
			if self.parent:
				self.parent.align()

		if "height" in self.overridden:
			self.h = self.attr["height"]
			if self.parent:
				self.parent.align()


	def mouseLeave(self, e, args):
		for attr, value in self.overridden.iteritems():
			self.attr[attr] = value

		if "width" in self.overridden:
			self.w = self.attr["width"]
			if self.parent:
				self.parent.align()

		if "height" in self.overridden:
			self.h = self.attr["height"]
			if self.parent:
				self.parent.align()

	def draw(self, screen):
		pass

class Button(Component):
	defaults = {
		"text": ""
	}

	def __init__(self, **args):
		super(Button, self).__init__(**args)

	def parseAttr(self):
		super(Button, self).parseAttr()

		for attr, value in Button.defaults.iteritems():
			self.attr.setdefault(attr, value)

		self.text = self.attr["text"]

	def draw(self, screen):
		pygame.draw.rect(screen, self.attr["background_colour"], (self.pos.x, self.pos.y, self.w, self.h), 0)
		pygame.draw.rect(screen, self.attr["border_colour"], (self.pos.x, self.pos.y, self.w, self.h), 2)
		
		text = Menu.font.render(self.text, 0, self.attr["colour"])
		textRect = text.get_rect()
		screen.blit(text, (self.pos.x + self.w/2 - textRect[2] / 2, self.pos.y + self.h / 2 - textRect[3] / 2))

class Image(Component):
	def __init__(self, **args):
		super(Image, self).__init__(**args)

	def parseAttr(self):
		super(Image, self).parseAttr()

		self.image = None
		if "image" in self.attr:
			self.image = self.attr["image"]
		elif "src" in self.attr:
			self.load(self.attr["src"])

	def load(self, src):
		self.image = resourceManager.loadImage(src)

		imgRect = self.image.get_rect()
		self.w = imgRect[2]
		self.h = imgRect[3]

	def draw(self, screen):
		screen.blit(self.image, (self.pos.x, self.pos.y))

class Container(Component):
	# align
	# 0 = CENTER
	# layout
	# 0 = VERTICAL
	def __init__(self, **args):
		super(Container, self).__init__(**args)
		self.components = []

	def addComponent(self, component):
		component.parent = self
		self.components.append(component)
		self.align()

	def align(self):
		if self.parent:
			totW, totH = 0, 0

			for i, c in enumerate(self.components):
				padding = c.attr["padding"]
				if c.w > totW:
					totW = c.w
				totH += c.h

			self.w = totW
			self.h = totH

			self.pos.x = self.parent.pos.x + self.parent.w / 2 - totW / 2
			self.pos.y = self.parent.pos.y + self.parent.h / 2 - totH / 2

			cury = self.pos.y
			for i, c in enumerate(self.components):
				c.pos.y = cury
				cury += c.h 
		
		for c in self.components:
			c.align()

	def update(self):
		super(Container, self).update()

		for c in self.components:
			c.update()

	def draw(self, screen):
		if self.attr["background_colour"]:
			pygame.draw.rect(screen, self.attr["background_colour"], (self.pos.x, self.pos.y, self.w, self.h))
		
		for c in self.components:
			c.draw(screen)

class View(object):
	def __init__(self):
		self.components = []
		self.parent = None

	def focus(self):
		self.doLayout()

	def blur(self):
		self.cleanLayout()

	def doLayout(self):
		pass

	def addComponent(self, component):
		self.components.append(component)

	def cleanLayout(self):
		self.components = []

	def update(self):
		for c in self.components:
			c.update()

	def draw(self, screen):
		for c in self.components:
			c.draw(screen)

class Menu(object):
	def __init__(self):
		self.stateProvider = StateProvider()
		self.views = []
		self.currentView = None
		self.config()
		Menu.font = pygame.font.Font("./assets/pixelated.ttf", 30)

	def config(self):
		pass

	def close(self):
		for view in self.views:
			view.cleanLayout()

	def draw(self, screen):
		if self.currentView:
			self.currentView.draw(screen)

	def update(self):
		if self.currentView:
			self.currentView.update()

	def addView(self, state):
		self.views.append(state.view)
		state.view.parent = self
		self.stateProvider.state(state)

	def focusView(self, newView):
		if newView:
			if self.currentView: self.currentView.blur()

			self.currentView = newView
			self.currentView.focus()

	def go(self, state):
		nextView = self.stateProvider.go(state)
		self.focusView(nextView)

	def back(self):
		nextView = self.stateProvider.back()
		self.focusView(nextView)


class State:
	def __init__(self, state, view):
		self.state = state
		self.view = view
		self.parent = None
		self.children = {}

class StateProvider:
	def __init__(self):
		self.currentState = None
		self.states = {}

	def go(self, newState):
		nodes = filter(lambda n: n, newState.split("."))

		if nodes[0] in self.states:
			nextNode = self.states[nodes[0]]
			if newState == nextNode.state:
				self.currentState = nextNode
				return self.currentState.view

			curNode = nextNode.children
		else:
			return None

		for node in nodes[1:]:			
			if node not in curNode:
				return None

			nextNode = curNode[node]
			if newState == nextNode.state:
				self.currentState = nextNode
				return self.currentState.view

			curParent = nextNode
			curNode = nextNode.children

		return None

	def state(self, newState):
		nodes = filter(lambda n: n, newState.state.split("."))

		if nodes[0] in self.states:
			curParent = self.states[nodes[0]]
			curNode = self.states[nodes[0]].children
		else:
			self.states[nodes[0]] = newState
			return True

		for node in nodes[1:]:
			if node not in curNode:
				newState.parent = curParent
				curNode[node] = newState
				
				return True

			nextNode = curNode[node]
			curParent = nextNode
			curNode = nextNode.children
		return False

	def back(self):
		if self.currentState.parent:
			self.currentState = self.currentState.parent
			return self.currentState.view
		return None