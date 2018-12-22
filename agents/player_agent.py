import pygame
import helpers
import world
from agents.agent import Agent
import sprites

class PlayerAgent(Agent):
    def __init__(self, x, y, width, height, controller):
        Agent.__init__(self, x, y, width, height, controller, sprites.mario)
        self._type = 'Player'
