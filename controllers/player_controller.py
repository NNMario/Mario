import controllers.controller
import environment
import random


class RandomController(controllers.controller.Controller):
    def __init__(self):
        controllers.controller.Controller.__init__(self)
        self.possible_actions = [
            environment.ACTION_NONE,
            environment.ACTION_FORWARD,
            environment.ACTION_BACK,
            environment.ACTION_JUMP
        ]

    def get_actions(self, agent, world_state):
        return [random.choice(self.possible_actions)]


class KeyBoardController(controllers.controller.Controller):
    def __init__(self):
        controllers.controller.Controller.__init__(self)
        self.current_actions = [environment.ACTION_NONE]

    def get_actions(self, agent, world_state):
        return self.current_actions
