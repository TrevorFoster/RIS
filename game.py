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

    running, full, music = True, False, True

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
        Window.screen.fill((0, 0, 0))

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

buttonStyle = {
    "background_colour": (100, 100, 100),
    "border_colour": (60, 60, 60),
    "colour": (255, 255, 255),
    "padding": 15,
    "hover": {
        "background_colour": (60, 60, 60),
        "border_colour": (100, 100, 100)
    }
}

class MainView(View):
    

    def doLayout(self):
        mainContainer = Container(width=Window.windw, height=Window.windh)
        middleContainer = Container()

        title = Image(src="./assets/RectangleTitle.png")
        startButton = Button(width=400, height=80, text="Start!", **buttonStyle)
        optionsButton = Button(width=400, height=80, text="Options", **buttonStyle)
        scoresButton = Button(width=400, height=80, text="High Scores", **buttonStyle)
        exitButton = Button(width=400, height=80, text="Exit", **buttonStyle)

        def startButtonClicked(e, args):
            print "HEY THERE"

        startButton.onClick.register(startButtonClicked)

        def optionsButtonClicked(e, args):
            args[0].go("main.options")

        optionsButton.onClick.register(optionsButtonClicked, self.parent)


        def exitButtonClicked(e, args):
            Game.running = False

        exitButton.onClick.register(exitButtonClicked)

        middleContainer.addComponent(title)
        middleContainer.addComponent(startButton)
        middleContainer.addComponent(optionsButton)
        middleContainer.addComponent(scoresButton)
        middleContainer.addComponent(exitButton)

        mainContainer.addComponent(middleContainer)

        self.addComponent(mainContainer)

class OptionView(View):
    def doLayout(self):
        mainContainer = Container(width=Window.windw, height=Window.windh)
        middleContainer = Container()

        fullToggle = Button(width=400, height=80, text="Toggle Fullscreen", **buttonStyle)
        musicToggle = Button(width=400, height=80, text=("Music: " + ("On" if Game.music else "Off")), **buttonStyle)
        backButton = Button(width=400, height=80, text="Back", **buttonStyle)

        fullToggle.onClick.register(self.toggleFullscreen)
        musicToggle.onClick.register(self.toggleMusic, musicToggle)
        backButton.onClick.register(self.backClicked)

        middleContainer.addComponent(fullToggle)
        middleContainer.addComponent(musicToggle)
        middleContainer.addComponent(backButton)

        mainContainer.addComponent(middleContainer)

        self.addComponent(mainContainer)

    def backClicked(self, e, args):
        self.parent.back()

    def toggleFullscreen(self, e, args):
        Game.full = not Game.full

    def toggleMusic(self, e, args):
        print args[0]
        Game.music = not Game.music
        args[0].text = "Music: " + ("On" if Game.music else "Off")

class ScoreView(View):
    def doLayout(self):
        button1 = Button(pos=Vector2(0, 0), width=200, height=100, text="SECOND")

        def button1Clicked():
            print button1.text

        button1.onClick.register(button1Clicked, self)



class MainMenu(Menu):
    def __init__(self):
        super(MainMenu, self).__init__()

    def config(self):
        self.addView(State("main", MainView()))
        self.addView(State("main.options", OptionView()))
        self.addView(State("main.scores", ScoreView()))

        self.go("main")
