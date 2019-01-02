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

    def draw_rect(self, rect, viewport_x, color, width=0):
        cp = rect.copy()
        cp.x -= viewport_x
        pygame.draw.rect(self.win, color, cp, width)

    def draw(self, env: environment.Environment):
        """ Draws the background image and initiates drawing of
            all the objects in the game
        :return: None
        """
        self.win.blit(sprites.background, (0, 0))
        world_rect = pygame.Rect((env.viewport_x, 0, self.w_width, self.w_height))
        # Draw the platforms
        for platform in env.platforms:
            if world_rect.colliderect(platform):
                self.draw_rect(platform, env.viewport_x, (200, 200, 200))

        for gap in env.gaps:
            if world_rect.colliderect(gap):
                self.draw_rect(gap, env.viewport_x, (20, 20, 20), 3)
        # Draw the player
        self.draw_rect(env.player_agent.rect, env.viewport_x, (100, 100, 100))
        self.draw_rect(env.player_agent.first_rect, env.viewport_x, (34, 139, 34), 2)
        self.draw_rect(env.player_agent.second_rect, env.viewport_x, (32, 178, 170), 2)
        self.draw_rect(env.player_agent.third_rect, env.viewport_x, (124, 252, 0), 1)

        for agent in env.agents:
            new_rect = agent.rect.copy()
            new_rect.x -= env.viewport_x
            # self.win.blit(self.image, new_rect)

        self.draw_rect(env.princess, env.viewport_x, (200, 0, 0), 2)

        myfont = pygame.font.SysFont('Comic Sans MS', 30)
        textsurface = myfont.render(str(env.score), False, (255, 255, 255))
        self.win.blit(textsurface, (10, 5))
        pygame.display.update()

    def uninit(self):
        pygame.quit()
