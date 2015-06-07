from game import Game
from threading import Timer
import random

class Weapon(object):
    def __init__(self, owner=None):
        self.owner = owner
        self.shooting = False
        self.timer = None

    def regulateShooting(self):
        self.shoot()
        if self.shooting:
            self.timer = Timer(self.shotInterval / 1000.0, self.regulateShooting, ())
            self.timer.start()

    def startShooting(self):
        if not self.shooting:
            self.shooting = True
            self.shoot()
            self.timer = Timer(self.shotInterval / 1000.0, self.regulateShooting, ())
            self.timer.start()

    def stopShooting(self):
        if self.timer != None:
            self.shooting = False
            self.timer.cancel()

    def shoot(self):
        pass

class SingleSquare(Weapon):
    def __init__(self, owner):
        super(SingleSquare, self).__init__(owner)
        self.name = "SINGLE SQUARE"
        self.dps = 8
        self.shotInterval = 380
        self.shotSpeed = 6
   
    def shoot(self):
        midiout.set_instrument(127)
        midiout.note_on(random.randint(65, 68), 70)
        stats[0] += 1
        
        projectiles = Game.projectiles
        projectiles.append(NormalBullet(self.owner.aimerPos.x - 2, self.owner.aimerPos.y - 2, 9, 9, self.dps,
         (random.randint(1, 255), random.randint(1, 255), random.randint(1, 255)), self.owner.angle, self.shotSpeed))

class SpreadSquare(Weapon):
    def __init__(self, owner):
        super(SpreadSquare, self).__init__(owner)
        self.name = "SPREAD SQUARE"
        self.dps = 8
        self.shotInterval = 380
        self.shotSpeed = 6
   
    def shoot(self):
        midiout.set_instrument(127)
        midiout.note_on(random.randint(65, 68), 70)
        stats[0] += 1

        projectiles = Game.projectiles
        projectiles.append(NormalBullet(self.owner.aimerPos.x - 2, self.owner.aimerPos.y - 2, 5, 5, self.dps,
         (random.randint(1, 255), random.randint(1, 255), random.randint(1, 255)), self.owner.angle, self.shotSpeed))
        projectiles.append(NormalBullet(self.owner.aimerPos.x - 2, self.owner.aimerPos.y - 2, 5, 5, self.dps, (random.randint(1, 255),
         random.randint(1, 255), random.randint(1, 255)), self.owner.angle - math.radians(random.randint(6, 8)), self.shotSpeed))
        projectiles.append(NormalBullet(self.owner.aimerPos.x - 2, self.owner.aimerPos.y - 2, 5, 5, self.dps, (random.randint(1, 255),
         random.randint(1, 255), random.randint(1, 255)), self.owner.angle + math.radians(random.randint(6, 8)), self.shotSpeed))

class MachineSquare(Weapon):
    def __init__(self, owner):
        super(MachineSquare, self).__init__(owner)
        self.name = "MACHINE SQUARE"
        self.dps = 1.4
        self.shotInterval = 100
        self.shotSpeed = 6
   
    def shoot(self):
        midiout.set_instrument(127)
        midiout.note_on(random.randint(65, 68), 70)
        stats[0] += 1

        projectiles = Game.projectiles
        projectiles.append(NormalBullet(self.owner.aimerPos.x - 2, self.owner.aimerPos.y - 2, 5, 5, self.dps, 
            (random.randint(1, 255), random.randint(1, 255), random.randint(1, 255)), self.owner.angle, self.shotSpeed))

class ExplosiveSquare(Weapon):
    def __init__(self, owner):
        super(ExplosiveSquare, self).__init__(owner)
        self.name = "EXPLOSIVE SQUARE"
        self.dps = 25.0
        self.shotInterval = 1200
        self.shotSpeed = 6
   
    def shoot(self):
        midiout.set_instrument(127)
        midiout.note_on(random.randint(65, 68), 70)
        stats[0] += 1
        
        projectiles = Game.projectiles
        projectiles.append(ExplosiveBullet(self.owner.aimerPos.x - 2, self.owner.aimerPos.y - 2, 11, 11, self.dps, 
            (random.randint(1, 255), random.randint(1, 255), random.randint(1, 255)), self.owner.angle, 0))