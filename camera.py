import pygame
from helpers import Vector2


class Camera:
    def __init__(self, size, windw, windh):
        self.x = (windw / 2 - ((windw / 2) * size))
        self.y = (windh / 2 - ((windh / 2) * size))
        self.offset = Vector2(0, 0)
        self.w = ((windw / 2) * size) * 2
        self.h = ((windh / 2) * size) * 2
        self.ww = windw
        self.wh = windh

    def update(self, plyr):
        pr = pygame.Rect(plyr.pos.x - self.offset.x, plyr.pos.y - self.offset.y, plyr.w, plyr.h)
        cr = pygame.Rect(self.x, self.y, self.w, self.h)
        if pr.colliderect(cr):
            rs = pygame.Rect((cr[0] + cr[2], cr[1]), (self.ww - cr[2], cr[3]))
            ls = pygame.Rect((0, cr[1]), (cr[0], cr[3]))
            tp = pygame.Rect((cr[0], 0), (cr[2], cr[1]))
            bt = pygame.Rect(
                (cr[0], cr[1] + cr[3] - 2), (cr[2], self.wh - cr[1]))
            if (pr.colliderect(rs)):
                self.offset.x += plyr.maxSpeed
            elif (pr.colliderect(ls)):
                self.offset.x -= plyr.maxSpeed
            if (pr.colliderect(tp)):
                self.offset.y -= plyr.maxSpeed
            elif (pr.colliderect(bt)):
                self.offset.y += plyr.maxSpeed
        else:
            self.offset += plyr.velocity

    def draw(self):
        pygame.draw.rect(screen, (255, 255, 255), (self.x, self.y, self.w, self.h), 2)