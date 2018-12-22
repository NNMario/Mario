import pygame
import config
import sprites
import world
from controllers.player_controller import RandomController
from controllers.player_controller import KeyBoardController


class Game:
    def __init__(self):
        pygame.init()
        pygame.font.init()
        self.win = pygame.display.set_mode((config.__WIDTH__, config.__HEIGHT__))
        pygame.display.set_caption("marIO")
        sprites.setup()

        self.run = True
        self.w_height = config.__HEIGHT__
        self.w_width = config.__WIDTH__
        self.world = None
        sprites.background = pygame.transform.scale(sprites.background, (self.w_width, self.w_height))

    def draw(self):
        self.win.blit(sprites.background, (0, 0))
        self.world.draw(self.win)

    def start(self):
        while self.run:
            current_controller = KeyBoardController()
            # rand_ctrl = RandomController()
            # self.world = world.World((self.w_width, self.w_height), keyboard)
            self.world = world.World((self.w_width, self.w_height), current_controller)
            self.world.generate()

            while self.run and not self.world.ended:
                clock = pygame.time.Clock()
                clock.tick_busy_loop(60)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.run = False
                        print('exit')

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

                self.world.tick()
                self.draw()
                pygame.display.update()

        pygame.quit()


def main():
    game = Game()
    game.start()


if __name__ == '__main__':
    main()
