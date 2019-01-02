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

    def get_action(self, env):
        return [random.choice(self.possible_actions)]


class KeyBoardController(controllers.controller.Controller):
    def __init__(self):
        controllers.controller.Controller.__init__(self)
        self.current_actions = [environment.ACTION_NONE]

    def get_action(self, env):
        return self.current_actions
