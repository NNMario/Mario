import pygame
import config
import sprites


class SimpleObject(pygame.sprite.Sprite):
    """ This sprite won't be drawn, but has to be in some group
    For ex: kill_block
    """
    def __init__(self, x, y, width, height):
        pygame.sprite.Sprite.__init__(self)
        self.rect = pygame.Rect((x, y, width, height))


class Drawable(pygame.sprite.Sprite):
    """ This sprite will be drawn, it gets a sprite parameter (from the sprites module)
    """
    def __init__(self, x, y, width, height, sprite=None):
        pygame.sprite.Sprite.__init__(self)
        self.image = sprite
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y

    def draw(self, win, view_x=0):
        new_rect = self.rect.copy()
        new_rect.x -= view_x
        win.blit(self.image, new_rect)


class Block(Drawable):
    def __init__(self, x, y, width, height):
        Drawable.__init__(self, x, y, width, height, sprites.block)
