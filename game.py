import pygame, random
from pygame.locals import *
from menu import *
from helpers import Keys, Mouse, Constants
from camera import Camera
from player import Player
from managers import *

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
    particles = []
    coins = []  

    running, full, music = True, False, True
    player = None
    paused = True
    clock = pygame.time.Clock()

    @staticmethod
    def init():
        Window.init()
        Game.cam = Camera(0.4, Window.windw, Window.windh)
        Game.menu = MainMenu()
        spaceObjectManager.load()

    @staticmethod
    def start():
        Game.player = Player(Window.windw / 2, Window.windh / 2, 20, 20, [random.randint(1, 255) for i in range(3)], Constants.MAXPLAYERSPEED, 100)
        Game.cam.offset = Vector2(0, 0)
        Game.menu = None
        Game.paused = False

    @staticmethod
    def exitGame():
        Game.player = None
        Game.paused = True
        Game.menu = MainMenu()

    @staticmethod
    def pause():
        Game.paused = True
        Game.menu = PauseMenu()

    @staticmethod
    def unpause():
        Game.paused = False
        Game.menu = None

    @staticmethod
    def update():
        if not Game.running: return False

        Keys.update()
        Mouse.update()
        for event in pygame.event.get():
            if event.type == QUIT:
                return False
        
        if Keys.get(K_ESCAPE).pressedReleased:
            Game.pause()

        spaceObjectManager.update(Game.cam.offset, Window.windw, Window.windh)
        if not Game.paused:
            projectileManager.update()
            particleManager.update()
            enemyManager.update(Game.player, Game.cam.offset, Window.windw, Window.windh)
            alive = Game.player.update(Game.cam.offset)
            Game.cam.update(Game.player)

        if Game.menu:
            Game.menu.update()

        millis = Game.clock.tick(200)
        GameTimer.tick(millis)

        return True

    @staticmethod
    def draw():
        Window.screen.fill((0, 0, 0))

        spaceObjectManager.draw(Window.screen, Game.cam.offset)
        projectileManager.draw(Window.screen, Game.cam.offset)
        particleManager.draw(Window.screen, Game.cam.offset)

        enemyManager.draw(Window.screen, Game.cam.offset)

        if Game.player:
            Game.player.draw(Window.screen, Game.cam.offset)

        if Game.menu:
            Game.menu.draw(Window.screen)

        pygame.display.update()

    @staticmethod
    def drawCoins():
        for coin in Game.coins:
            coin.draw(cam.offset)

buttonStyle = {
    "background_colour": (100, 100, 100),
    "border_colour": (60, 60, 60),
    "colour": (255, 255, 255),
    "padding": 15,
    "width": 400,
    "height": 80,
    "hover": {
        "background_colour": (60, 60, 60),
        "border_colour": (100, 100, 100),
        "width": 390
    }
}

class MainView(View):
    def doLayout(self):
        mainContainer = Container(width=Window.windw, height=Window.windh)
        middleContainer = Container()

        title = Image(src="./assets/RectangleTitle.png")
        startButton = Button(text="Start!", **buttonStyle)
        optionsButton = Button(text="Options", **buttonStyle)
        scoresButton = Button(text="High Scores", **buttonStyle)
        exitButton = Button(text="Exit", **buttonStyle)

        startButton.onClick.register(self.startButtonClicked)
        optionsButton.onClick.register(self.optionsButtonClicked, self.parent)
        exitButton.onClick.register(self.exitButtonClicked)

        middleContainer.addComponent(title)
        middleContainer.addComponent(startButton)
        middleContainer.addComponent(optionsButton)
        middleContainer.addComponent(scoresButton)
        middleContainer.addComponent(exitButton)

        mainContainer.addComponent(middleContainer)

        self.addComponent(mainContainer)

    def startButtonClicked(self, e, args):
            Game.start()

    def optionsButtonClicked(self, e, args):
            args[0].go("main.options")

    def exitButtonClicked(self, e, args):
            Game.running = False

class OptionsView(View):
    def doLayout(self):
        mainContainer = Container(width=Window.windw, height=Window.windh)
        middleContainer = Container()

        fullToggle = Button(text="Toggle Fullscreen", **buttonStyle)
        musicToggle = Button(text=("Music: " + ("On" if Game.music else "Off")), **buttonStyle)
        backButton = Button(text="Back", **buttonStyle)

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
        self.addView(State("main.options", OptionsView()))
        self.addView(State("main.scores", ScoreView()))

        self.go("main")

class MainPauseView(View):
    def doLayout(self):
        mainContainer = Container(width=Window.windw, height=Window.windh)
        middleContainer = Container()

        resumeButton = Button(text="Resume", **buttonStyle)
        optionsButton = Button(text="Options", **buttonStyle)
        exitButton = Button(text="Exit to Main Menu", **buttonStyle)

        resumeButton.onClick.register(self.resumeClicked)
        optionsButton.onClick.register(self.optionsClicked, self.parent)
        exitButton.onClick.register(self.exitClicked)

        middleContainer.addComponent(resumeButton)
        middleContainer.addComponent(optionsButton)
        middleContainer.addComponent(exitButton)

        mainContainer.addComponent(middleContainer)
        self.addComponent(mainContainer)

    def resumeClicked(self, e, args):
        Game.unpause()

    def optionsClicked(self, e, args):
        args[0].go("main.options")

    def exitClicked(self, e, args):
        Game.exitGame()


class PauseMenu(Menu):
    def __init__(self):
        super(PauseMenu, self).__init__()

    def config(self):
        self.addView(State("main", MainPauseView()))
        self.addView(State("main.options", OptionsView()))

        self.go("main")
