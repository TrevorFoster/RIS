from helpers import Vector2
from spritesheet import Spritesheet, Animation

class Coin:
    animation = Animation(Spritesheet("./assets/coin.png").extractFrames([8, 1]))
    frame = None

    def __init__(self, x, y, worth):
        self.pos = Vector2(x, y)
        self.worth = worth

    @staticmethod
    def update():
        Coin.frame = Coin.animation.next()

    def collide(self):
        r = pygame.Rect(self.x, self.y, self.img.get_rect()[2], self.img.get_rect()[3])
        if r.colliderect(plr):
            midiout.set_instrument(118)
            midiout.note_on(random.randint(100, 102), 112)
            midiout.note_on(random.randint(70, 75), 112)
            return True
        return False

    def draw(self, offset):
        screen.blit(frame, (self.pos.x - offset.x, self.pos.y - offset.y))