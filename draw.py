import pygame
import environment
from graphics import sprites
import config


class Drawer:
    def __init__(self, width, height):
        pygame.init()
        pygame.font.init()
        self.win = pygame.display.set_mode((width, height))
        pygame.display.set_caption("marIO")
        self.w_height = height
        self.w_width = width
        # Create all the game sprites from the spritesheet
        sprites.setup()
        sprites.background = pygame.transform.scale(sprites.background, (self.w_width, self.w_height))
        # The position of the viewport in the game map

    def draw(self, env: environment.Environment):
        """ Draws the background image and initiates drawing of
            all the objects in the game
        :return: None
        """
        self.win.blit(sprites.background, (0, 0))
        # Draw the platforms
        for platform in env.platforms:
            pygame.draw.rect(self.win, (200, 200, 200), platform)

        for gap in env.gaps:
            pygame.draw.rect(self.win, (20, 20, 20), gap, 3)
        # Draw the player
        pygame.draw.rect(self.win, (100, 100, 100), env.player_agent.rect)

        for agent in env.agents:
            new_rect = agent.rect.copy()
            new_rect.x -= env.viewport_x
            #self.win.blit(self.image, new_rect)

        #
        #    world_rect = pygame.Rect((self.view_x, 0, self.width, self.height))
        #    if sprite.rect.colliderect(world_rect):
        #        sprite.draw(win, self.view_x)

        myfont = pygame.font.SysFont('Comic Sans MS', 30)
        textsurface = myfont.render(str(env.score), False, (255, 255, 255))
        self.win.blit(textsurface, (10, 5))

        pygame.display.update()

    def uninit(self):
        pygame.quit()