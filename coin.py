from game import Game
from spritesheet import Spritesheet

class Coin:
    frames = Spritesheet("./assets/coin.png").extractFrames([8, 1])
    def __init__(self, x, y, worth, img):
        self.x = x
        self.y = y
        self.worth = worth
        self.img = img

    def collide(self):
        r = pygame.Rect(self.x, self.y, self.img.get_rect()[2], self.img.get_rect()[3])
        if r.colliderect(plr):
            midiout.set_instrument(118)
            midiout.note_on(random.randint(100, 102), 112)
            midiout.note_on(random.randint(70, 75), 112)
            Game.player.score += self.worth
            return True
        return False

    def draw(self, frame, offset):
    	frame = Coin.frames[Game.frame]
        screen.blit(frame.img, (self.x - offset.x, self.y - offset.y))