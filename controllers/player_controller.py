import controllers.controller
import world
import random


class RandomController(controllers.controller.Controller):
    def __init__(self):
        controllers.controller.Controller.__init__(self)
        self.possible_actions = [
            world.ACTION_NONE,
            world.ACTION_FORWARD,
            world.ACTION_BACK,
            world.ACTION_JUMP
        ]

    def get_actions(self, agent, world_state):
        return [random.choice(self.possible_actions)]


class KeyBoardController(controllers.controller.Controller):
    def __init__(self):
        controllers.controller.Controller.__init__(self)
        self.current_actions = [world.ACTION_NONE]

    def get_actions(self, agent, world_state):
        return self.current_actions
