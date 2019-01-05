from agents.agent import Agent
from graphics import sprites
import pygame

class EnemyAgent(Agent):
    def __init__(self, x, y, width, height):
        Agent.__init__(self, x, y, width, height)
        self._type = 'Enemy'
        self.top_rect = pygame.Rect((x - 5, y - 5, self.rect.width + 5, 5))
