import random
from copy import deepcopy

import pygame
import config
from agents.player_agent import PlayerAgent

ACTION_NONE = 3
ACTION_FORWARD = 0
ACTION_BACK = 2
ACTION_JUMP = 1

actions = [
    #ACTION_NONE,
    ACTION_FORWARD,
   # ACTION_BACK,
    ACTION_JUMP
]


class Environment:
    """ The state keeper, has all the information about the world, including
    agents, platforms, world sizes, player, etc.
    At each loop of the game, the world gets updated

    """
    def __init__(self, w_width, w_height):
        self.width = w_width  # Irrelevant, will be recalculated upon generation
        self.w_width = w_width
        self.height = w_height
        self.block_length = 0
        self.ground_height = self.height - config.__BLOCK_SIZE__

        # Groups define similar objects and have their purpose
        self.agents = []  # Used for making actions on each subject
        self.platforms = []  # Used to generate rewards on the right place
        self.lose_triggers = []  # Will make the player lose on collide
        self.gaps = []
        self.player_agent = None
        self.princess = None
        self.ended = False
        self.is_win = False
        self.score = 0
        self.viewport_x = 0

    def generate(self):
        self.agents.clear()
        self.platforms.clear()
        self.lose_triggers.clear()
        self.gaps.clear()

        self.ended = False
        self.is_win = False
        self.score = False
        self.player_agent = None
        self.princess = None
        self.viewport_x = 0
        self._generate()

    def snapshot(self):
        return deepcopy(self)

    def _generate(self):
        """ Instantiate all the blocks, enemies, rewards
        The world with should be chosen at random and is given by the block_length variable
        0. All the floor blocks with random gaps of length 2
        1. Under the floor blocks, there is a kill_block object, that will make the player lose on contact
        2. The princess, which is the reward object, gets placed in the last 10 blocks, the won't have any gaps

        :return: None
        """
        self.block_length = 200  # random.randint(400, 1000)
        self.width = self.block_length * config.__BLOCK_SIZE__
        # Add the floor platforms
        floor_x = 0
        floor_y = self.height - config.__BLOCK_SIZE__
        for i in range(self.block_length):
            block = pygame.Rect((floor_x, floor_y, config.__BLOCK_SIZE__, config.__BLOCK_SIZE__))
            self.platforms.append(block)
            if random.random() < 0.2 and i < self.block_length - config.__SAFE_LAST_BLOCKS__:
                gap = pygame.Rect((floor_x + config.__BLOCK_SIZE__, floor_y, config.__BLOCK_SIZE__,
                                   config.__BLOCK_SIZE__))
                self.gaps.append(gap)
                gap = pygame.Rect((floor_x + 2 * config.__BLOCK_SIZE__, floor_y, config.__BLOCK_SIZE__,
                                   config.__BLOCK_SIZE__))
                self.gaps.append(gap)
                floor_x += 3 * config.__BLOCK_SIZE__
            else:
                floor_x += config.__BLOCK_SIZE__

        # Add sprites that make the player lose on collision
        kill_block = pygame.Rect((0, self.height, self.block_length * config.__BLOCK_SIZE__, 50))
        self.lose_triggers.append(kill_block)

        self.princess = pygame.Rect(
            ((self.block_length - 10) * config.__BLOCK_SIZE__,
             floor_y - config.__PRINCESS_HEIGHT__,
             config.__PRINCESS_WIDTH__,
             config.__PRINCESS_HEIGHT__)
        )
        self._create_agents()

    def _create_agents(self):
        player_x = 5
        player_y = self.ground_height - config.__PLAYER_HEIGHT__
        self.player_agent = PlayerAgent(
            player_x,
            player_y,
            config.__PLAYER_WIDTH__,
            config.__PLAYER_HEIGHT__,
        )

        self.player_agent.set_velocity(3, 10)
        self.player_agent.set_acceleration(0, config.__GRAVITY__)

    def tick(self, agent_action):
        self.player_agent.perform_action(agent_action)
        self.player_agent.tick(self)
        for agent in self.agents:
            agent.tick(self)

        center_x = self.viewport_x + self.w_width / 2.0
        dx = self.player_agent.rect.x - center_x
        if dx > 0 and self.viewport_x + self.w_width < self.width:
            self.viewport_x += dx

        for trigger in self.lose_triggers:
            if self.player_agent.rect.colliderect(trigger):
                self.end()
                return

        hits = self.player_agent.rect.colliderect(self.princess)
        if hits:
            self.win()
            return

    def end(self):
        self.ended = True
        self.is_win = False

    def win(self):
        self.ended = True
        self.is_win = True
