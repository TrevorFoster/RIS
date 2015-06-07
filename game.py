import pygame
from pygame.locals import *
from camera import Camera
from menu import *
from helpers import Keys, Mouse

class Window:
    windw, windh = 800, 600

    @staticmethod
    def init():
        Window.screen = pygame.display.set_mode((Window.windw, Window.windh), 0, 32)
        Window.maxres = pygame.display.list_modes()[0]
        pygame.display.set_caption("SQUARES IN SPACE")
        ico = pygame.image.load("./assets/Icon.png").convert_alpha()
        pygame.display.set_icon(ico)

class Game:
    projectiles = []
    particles = []
    planets = []
    coins = []
    stars = []
    enemies = []
    running = True

    @staticmethod
    def init():
        Window.init()
        Game.cam = Camera(0.6, Window.windw, Window.windh)
        Game.menu = MainMenu()

    @staticmethod
    def update():
        if not Game.running: return False

        for event in pygame.event.get():
            if event.type == QUIT:
                return False
        
        Keys.update()
        Mouse.update()

        Game.menu.update()

        return True

    @staticmethod
    def draw():
        Window.screen.fill((255,255,255))

        Game.drawPlanets()
        Game.drawStars()
        Game.drawCoins()
        Game.drawProjectiles()
        Game.drawParticles()
        Game.drawEnemies()

        Game.menu.draw(Window.screen)
        pygame.display.update()

    @staticmethod
    def drawPlanets():
        for planet in Game.planets:
            if planet.x - outright + planet.zx < windw and (planet.x + planet.img.get_rect()[2]) - outright + planet.zx > 0 and planet.y - outbottom + planet.zy < windh and (planet.y + planet.img.get_rect()[3]) - outbottom + planet.zy > 0:
                screen.blit(planet.img, (planet.x - outright + planet.zx, planet.y - outbottom + planet.zy))

    @staticmethod
    def drawStars():
        for star in Game.stars:
            pygame.draw.rect(
                screen, star.colour, (star.x - outright + star.zx, star.y - outbottom + star.zy, star.w, star.h))

    @staticmethod
    def drawCoins():
        for coin in Game.coins:
            coin.draw(cam.offset)

    @staticmethod       
    def drawProjectiles():
        for p in Game.projectiles:
           p.draw()

    @staticmethod
    def drawParticles():
        for i in Game.particles:
            if i.colour != "r":
                pygame.draw.rect(
                    screen, (i.colour), ((i.x - outright, i.y - outbottom), (i.s, i.s)), 0)
            else:
                pygame.draw.rect(screen, (random.randint(0, 255), random.randint(
                    0, 255), random.randint(0, 255)), ((i.x - outright, i.y - outbottom), (i.s, i.s)), 0)
    @staticmethod
    def drawEnemies():
        for e in Game.enemies:
            e.draw()

class MainView(View):
    def doLayout(self):
        mainContainer = Container(0, 0, Window.windw, Window.windh)
        middleContainer = Container(0, 0, 100, 100)

        startButton = Button(0, 0, 200, 100, "Start!")
        optionsButton = Button(0, 0, 200, 100, "Options")
        scoresButton = Button(0, 0, 300, 100, "High scores")
        exitButton = Button(0, 0, 200, 100, "Exit")

        @startButton.registerOnClick
        def startButtonClicked():
            print "HEY THERE"

        @exitButton.registerOnClick
        def startButtonClicked():
            Game.running = False

        middleContainer.addComponent(startButton)
        middleContainer.addComponent(optionsButton)
        middleContainer.addComponent(scoresButton)
        middleContainer.addComponent(exitButton)

        mainContainer.addComponent(middleContainer)

        self.components.append(mainContainer)

class ScoreView(View):
    def doLayout(self):
        button1 = Button(0, 0, 200, 100, "SECOND")

        @button1.registerOnClick
        def button1Clicked():
            print button1.text

class OptionView(View):
    def doLayout(self):
        button1 = Button(0, 0, 200, 100, "THIRD")

        @button1.registerOnClick
        def button1Clicked():
            print button1.text

class MainMenu(Menu):
    def __init__(self):
        super(MainMenu, self).__init__()

    def config(self):
        MainMenu.addView(State("main", MainView()))
        MainMenu.addView(State("main.scores", ScoreView()))
        MainMenu.addView(State("main.options", OptionView()))

        MainMenu.go("main")
