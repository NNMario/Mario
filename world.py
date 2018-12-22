import random

import pygame
import config
from agents.player_agent import PlayerAgent
from objects.object import SimpleObject, Block, Drawable
import sprites
import controllers.player_controller

ACTION_NONE = 0
ACTION_FORWARD = 1
ACTION_BACK = 2
ACTION_JUMP = 3


class World:
    """ The state keeper, has all the information about the world, including
    agents, platforms, world sizes, viewport position, player, etc.
    At each loop of the game, the world gets updated

    """
    def __init__(self, bounds, player_controller):
        # Groups define similar objects and have their purpose
        self.sprites = pygame.sprite.Group()  # Used for drawing everything
        self.agents = pygame.sprite.Group()  # Used for making actions on each subject
        self.platforms = pygame.sprite.Group()  # Used to generate rewards on the right place
        self.lose_triggers = pygame.sprite.Group()  # Will make the player lose on collide
        self.bounds = bounds
        self.width, self.height = bounds
        self.view_x = 0
        self.block_length = 0

        self.player_controller = player_controller
        player_x = 0
        player_y = self.height - config.__BLOCK_SIZE__ - config.__PLAYER_HEIGHT__
        self.player_subject = PlayerAgent(
            player_x,
            player_y,
            config.__PLAYER_WIDTH__,
            config.__PLAYER_HEIGHT__,
            self.player_controller
        )
        self.player_subject.set_velocity(3, 10)
        self.player_subject.set_acceleration(0, config.__GRAVITY__)
        self.agents.add(self.player_subject)
        self.sprites.add(self.player_subject)

        self.ended = False
        self.max_x = 0
        self.coins = 0
        self.score = 0

    def generate(self):
        """ Instantiate all the blocks, enemies, rewards
        The world with should be chosen at random and is given by the block_length variable
        0. All the floor blocks with random gaps of length 2
        1. Under the floor blocks, there is a kill_block object, that will make the player lose on contact
        2. The princess, which is the reward object, gets placed in the last 10 blocks, the won't have any gaps

        :return: None
        """
        self.block_length = 100  # random.randint(400, 1000)

        # Add the floor platforms
        floor_x = 0
        floor_y = self.height - config.__BLOCK_SIZE__
        for i in range(self.block_length):
            block = Block(floor_x, floor_y, config.__BLOCK_SIZE__, config.__BLOCK_SIZE__)
            self.platforms.add(block)
            self.sprites.add(block)
            if random.random() < 0.1 and i < self.block_length - config.__SAFE_LAST_BLOCKS__:
                floor_x += 3 * config.__BLOCK_SIZE__
            else:
                floor_x += config.__BLOCK_SIZE__

        # Add sprites that make the player lose on collision
        kill_block = SimpleObject(
            0,
            self.height,
            self.block_length * config.__BLOCK_SIZE__,
            50,
        )
        self.lose_triggers.add(kill_block)

        princess = Drawable(
            (self.block_length - 10) * config.__BLOCK_SIZE__,
            floor_y - config.__PRINCESS_HEIGHT__,
            config.__PRINCESS_WIDTH__,
            config.__PRINCESS_HEIGHT__,
            sprites.princess
        )
        self.sprites.add(princess)

    def tick(self):
        """ Update every object, viewport and score
        Checks if the player has hit a lose_trigger object. In the case, the game ends
        :return: None
        """
        for subject in self.agents:
            subject.tick(self)
            subject.update()

        hits = pygame.sprite.spritecollide(self.player_subject, self.lose_triggers, False)
        if hits:
            self.end()
            return

        center_x = self.view_x + self.width / 2.0
        dx = self.player_subject.rect.x - center_x
        if dx > 0 and self.view_x + self.width < self.block_length * config.__BLOCK_SIZE__:
            self.view_x += dx

        self.calculate_score()

    def end(self):
        self.ended = True

    def calculate_score(self):
        """ Score consists of the maximum X value that the player has been on
        added to the weighted amount of counts collected
        :return: None
        """
        self.max_x = max(self.max_x, self.player_subject.rect.x)
        self.score = self.max_x + 100 * self.coins

    def draw(self, win):
        """ Draw everything that is inside the viewport
        Also draws the score

        :param win: pygame screen instance
        :return: None
        """
        for sprite in self.sprites:
            world_rect = pygame.Rect((self.view_x, 0, self.width, self.height))
            if sprite.rect.colliderect(world_rect):
                sprite.draw(win, self.view_x)

        myfont = pygame.font.SysFont('Comic Sans MS', 30)
        textsurface = myfont.render(str(self.score), False, (255, 255, 255))
        win.blit(textsurface, (10, 5))
