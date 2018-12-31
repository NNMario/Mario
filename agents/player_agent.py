from agents.agent import Agent
from graphics import sprites


class PlayerAgent(Agent):
    def __init__(self, x, y, width, height):
        Agent.__init__(self, x, y, width, height)
        self._type = 'Player'
