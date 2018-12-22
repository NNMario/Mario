import pygame
import config
import sprites
import world
from controllers.player_controller import RandomController
from controllers.player_controller import KeyBoardController


class Game:
    def __init__(self):
        # Init all the components
        pygame.init()
        pygame.font.init()
        self.win = pygame.display.set_mode((config.__WIDTH__, config.__HEIGHT__))
        pygame.display.set_caption("marIO")
        # Create all the game sprites from the spritesheet
        sprites.setup()

        self.run = True
        self.w_height = config.__HEIGHT__
        self.w_width = config.__WIDTH__
        self.world = None
        sprites.background = pygame.transform.scale(sprites.background, (self.w_width, self.w_height))

    def draw(self):
        """ Draws the background image and initiates drawing of
        all the objects in the game
        :return: None
        """
        self.win.blit(sprites.background, (0, 0))
        self.world.draw(self.win)

    def start(self):
        """ Gameloop function, resets the game if it is ended and closes the window if the user pressed X
        At each loop (tick) the world updates and gets drawn
        The game runs at frames per second specified in the config (__FPS__)

        :return: None
        """
        # There can be multiple runs of the game, but if we press X -> it's ending
        while self.run:
            # The player agent will be controlled by the keyboard
            current_controller = KeyBoardController()

            # Initialize the game world
            self.world = world.World((self.w_width, self.w_height), current_controller)
            # Generate all the blocks, enemies
            self.world.generate()

            while self.run and not self.world.ended:
                clock = pygame.time.Clock()
                # Keep the game at 60 fps
                clock.tick_busy_loop(config.__FPS__)

                # poll events, see if we exit the game
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.run = False
                        print('exit')

                # If the player is controlled by keyboard, poll the keys and give actions
                if isinstance(current_controller, KeyBoardController):
                    keys_list = pygame.key.get_pressed()
                    actions = []
                    if keys_list[pygame.K_a]:
                        # keyboard.current_action = world.ACTION_BACK
                        actions.append(world.ACTION_BACK)
                    if keys_list[pygame.K_d]:
                        # keyboard.current_action = world.ACTION_FORWARD
                        actions.append(world.ACTION_FORWARD)
                    if keys_list[pygame.K_SPACE]:
                        # keyboard.current_action = world.ACTION_JUMP
                        actions.append(world.ACTION_JUMP)

                    if actions:
                        current_controller.current_actions = actions
                    else:
                        current_controller.current_actions = [ world.ACTION_NONE ]

                # Tick the world and every object in it
                self.world.tick()
                # Draw everything
                self.draw()
                pygame.display.update()

        pygame.quit()


def main():
    game = Game()
    game.start()


if __name__ == '__main__':
    main()
