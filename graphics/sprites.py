import pygame


# This class handles sprite sheets
# This was taken from www.scriptefun.com/transcript-2-using
# sprite-sheets-and-drawing-the-background
# I've added some code to fail if the file wasn't found..
# Note: When calling images_at the rect is the format:
# (x, y, x + offset, y + offset)

class Spritesheet(object):
    def __init__(self, filename):
        try:
            self.sheet = pygame.image.load(filename).convert()
        except pygame.error as message:
            print('Unable to load spritesheet image:', filename)
            raise SystemExit(message)

    # Load a specific image from a specific rectangle
    def image_at(self, rectangle, colorkey=None):
        """Loads image from x,y,x+offset,y+offset"""
        rect = pygame.Rect(rectangle)
        image = pygame.Surface(rect.size).convert()
        image.blit(self.sheet, (0, 0), rect)
        if colorkey is not None:
            if colorkey is -1:
                colorkey = image.get_at((0, 0))
            image.set_colorkey(colorkey, pygame.RLEACCEL)
        return image

    # Load a whole bunch of images and return them as a list
    def images_at(self, rects, colorkey=None):
        """Loads multiple images, supply a list of coordinates"""
        return [self.image_at(rect, colorkey) for rect in rects]

    # Load a whole strip of images
    def load_strip(self, rect, image_count, colorkey=None):
        """Loads a strip of images and returns them as a list"""
        tups = [(rect[0] + rect[2] * x, rect[1], rect[2], rect[3])
                for x in range(image_count)]
        return self.images_at(tups, colorkey)


background = None
sprites = None
block = None
mario = None
princess = None
coin = None
enemy = None
tube = None


def setup():
    global background, sprites, block, mario, princess, coin, enemy, tube
    background = pygame.image.load('sprites/background.png')
    sprites = Spritesheet('sprites/spritesheet.png')
    block = sprites.image_at((669, 533, 30, 30), colorkey=(255, 255, 255))
    mario = []
    for i in range(3):
        mario.append(sprites.image_at((346 + 3 * i + 15 * i, 8, 15, 15), colorkey=(255, 255, 255)))

    coin = [sprites.image_at((525, 534, 13, 16), colorkey=(255, 255, 255)),
            sprites.image_at((543, 534, 10, 16), colorkey=(255, 255, 255)),
            sprites.image_at((557, 534, 6, 16), colorkey=(255, 255, 255)),
            sprites.image_at((543, 534, 10, 16), colorkey=(255, 255, 255))]

    princess = sprites.image_at((823, 1105, 16, 31), colorkey=(255, 255, 255))

    enemy = [sprites.image_at((165, 724, 16, 16), colorkey=(255, 255, 255))]
    tube = sprites.image_at((566, 622, 13, 14), colorkey=(255, 255, 255))
