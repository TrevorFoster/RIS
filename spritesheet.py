import pygame

class Spritesheet:

    def __init__(self, filename):
        try:
            self.sheet = pygame.image.load(filename).convert()
        except pygame.error, message:
            print "Unable to load spritesheet image:", filename
            sys.exit(), message

    # Extract an image at the rectangle
    def imageAt(self, rectangle, colorkey=None):
        rect = pygame.Rect(rectangle)
        image = pygame.Surface(rect.size).convert()
        image.blit(self.sheet, (0, 0), rect)
        if colorkey != None:
            if colorkey != -1:
                colorkey = image.get_at((0, 0))
            image.set_colorkey(colorkey, pygame.RLEACCEL)
        return image

    # Extract all images in the rect list
    def imagesAt(self, rects, colorkey=None):
        return [self.imageAt(rect, colorkey) for rect in rects]

    def extractImages(self, dimensions):
        rec = self.sheet.get_rect()
        framew, frameh = rec[2] / dimensions[0], rec[3] / dimensions[1]
        points = []
        
        for y in range(dimensions[1]):
            for x in range(dimensions[0]):
                points.append((x * framew, y * frameh, framew, frameh))

        return self.imagesAt(points, colorkey=(0, 0, 0))

class Animation:
    def __init__(self, images):
        self.frames = images
        self.frame = 0

    def next(self):
        if self.frame >= len(self.images) - 1:
            self.frame = 0

        return self.frames[self.frame]

    def current(self):
        return self.frames[self.frame]