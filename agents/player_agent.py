from agents.agent import Agent
from graphics import sprites
import config

class PlayerAgent(Agent):
    def __init__(self, x, y, width, height):
        Agent.__init__(self, x, y, width, height)
        self._type = 'Player'
        self.first_rect = None
        self.second_rect = None
        self.third_rect = None
        self._update_rects()

    def _update_rects(self):
        self.first_rect = self.rect.copy()
        self.first_rect.width += config.__FIRST_RECT__
        self.first_rect.x -= config.__FIRST_RECT__
        self.first_rect.height += config.__FIRST_RECT__
        self.first_rect.y -= config.__FIRST_RECT__ / 2

        self.second_rect = self.rect.copy()
        self.second_rect.width += config.__SECOND_RECT__
        self.second_rect.x -= config.__SECOND_RECT__
        self.second_rect.height += config.__SECOND_RECT__
        self.second_rect.y -= config.__SECOND_RECT__ / 2

        self.third_rect = self.rect.copy()
        self.third_rect.width += config.__THIRD_RECT__
        self.third_rect.x -= config.__THIRD_RECT__
        self.third_rect.height += config.__THIRD_RECT__
        self.third_rect.y -= config.__THIRD_RECT__ / 2

    def tick(self, env):
        Agent.tick(self, env)
        self._update_rects()