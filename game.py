import pygame
import config
from controllers.player_controller import KeyBoardController
from controllers.q_learn_nn import DeepQLearning
from draw import Drawer
from environment import Environment
from environment import actions as Actions
import environment
import cProfile, pstats, io


class Game:
    def __init__(self):
        # Init all the components
        self.width = config.__WIDTH__
        self.height = config.__HEIGHT__
        self.run = True
        self.ticks = 0
        self.episodes = 0
        self.max_ticks = config.__MAX_TICKS__
        self.drawer = Drawer(self.width, self.height)
        self.environment = Environment(self.width, self.height)

    def start(self):
        """ Gameloop function, resets the game if it is ended and closes the window if the user pressed X
        At each loop (tick) the world updates and gets drawn
        The game runs at frames per second specified in the config (__FPS__)

        :return: None
        """
        # There can be multiple runs of the game, but if we press X -> it's ending

        # The player agent will be controlled by this
        current_controller = DeepQLearning(Actions)  # KeyBoardController()
        # current_controller = KeyBoardController()
        feed = config.__FEED__
        if feed:
            print('Feeding new data')
        else:
            print('No training')

        while self.run:
            # Generate all the blocks, enemies
            self.environment.generate()
            ticks = 0
            self.episodes += 1
            draw = False
            save = False
            load = False
            while self.run and not self.environment.ended:
                # clock = pygame.time.Clock()
                # Keep the game at 60 fps
                # clock.tick_busy_loop(config.__FPS__)

                # poll events, see if we exit the game
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.run = False
                        print('exit')

                keys_list = pygame.key.get_pressed()
                # If the player is controlled by keyboard, poll the keys and give actions
                if isinstance(current_controller, KeyBoardController):
                    actions = []
                    if keys_list[pygame.K_a]:
                        actions.append(environment.ACTION_BACK)
                    if keys_list[pygame.K_d]:
                        # keyboard.current_action = world.ACTION_FORWARD
                        actions.append(environment.ACTION_FORWARD)
                    if keys_list[pygame.K_SPACE]:
                        # keyboard.current_action = world.ACTION_JUMP
                        actions.append(environment.ACTION_JUMP)

                    if actions:
                        current_controller.current_actions = actions
                    else:
                        current_controller.current_actions = [environment.ACTION_NONE]
                if keys_list[pygame.K_RIGHT]:
                    config.__FPS__ += 20
                elif keys_list[pygame.K_LEFT]:
                    config.__FPS__ -= 20
                elif keys_list[pygame.K_c]:
                    draw = True
                elif keys_list[pygame.K_s]:
                    save = True
                elif keys_list[pygame.K_l]:
                    load = True
                elif keys_list[pygame.K_n]:
                    break

                # Tick the world and every object in it

                current_state = self.environment.snapshot()
                # Get action
                if isinstance(current_controller, KeyBoardController):

                    actions = current_controller.get_action(self.environment)
                    for action in actions:
                        self.environment.tick(action)
                else:
                    player_action = current_controller.get_action(self.environment)
                    self.environment.tick(player_action)
                    # Get new state
                    reward = current_controller.reward(self.environment, current_state)
                    self.environment.score = reward
                    # Save the state transition
                    current_controller.remember(current_state, player_action, reward, self.environment)

                ticks += 1
                # Draw everything
                if draw:
                    self.drawer.draw(self.environment)

                if ticks > self.max_ticks:
                    break
                if feed:
                    current_controller.done(self.episodes)
            self.ticks += ticks
            print(ticks, current_controller.last_acc, self.ticks)
            if save:
                current_controller.save()
                print('Saved')
            if load:
                current_controller.load()
                print('Loaded')
        self.drawer.uninit()


def main():
    # pr = cProfile.Profile()
    # pr.enable()

    game = Game()
    game.start()

    # pr.disable()
    # s = io.StringIO()
    # ps = pstats.Stats(pr, stream=s).sort_stats('cumulative')
    # ps.print_stats()
    # print(s.getvalue())


if __name__ == '__main__':
    main()
