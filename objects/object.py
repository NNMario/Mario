import pygame
import config
import sprites


class Drawable(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, sprite):
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
