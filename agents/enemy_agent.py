import random

from agents.agent import Agent
from graphics import sprites
import pygame


class EnemyAgent(Agent):
    def __init__(self, x, y, width, height):
        Agent.__init__(self, x, y, width, height)
        self._type = 'Enemy'
        self.top_rect = pygame.Rect((x - 2, y - 10, self.rect.width + 4, 10))
        self.actions = [2, 0]
        self.action_queue = []

    def tick(self, env):
        if not self.action_queue:
            self.action_queue.extend([random.choice(self.actions)] * 20)
        else:
            self.perform_action(self.action_queue[0])
            self.action_queue = self.action_queue[1:]
        #env = env.snapshot()
        #env.platforms += env.gaps
        Agent.tick(self, env)
        self.top_rect.x = self.rect.x - 2
        self.top_rect.y = self.rect.y - 10