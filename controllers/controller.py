import pygame
import environment


class Controller:
    def __init__(self):
        pass

    def get_action(self, env: environment.Environment):
        pass

    def learn(self):
        pass

    def remember(self, env: environment.Environment, action: environment.actions, reward: int, next_env: environment.Environment):
        pass

    def reward(self, env: environment.Environment, old_env: environment.Environment):
        pass

    def done(self):
        pass
