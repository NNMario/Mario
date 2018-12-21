import pygame
import config
import copy

pygame.init()
win = pygame.display.set_mode((config.__WIDTH__, config.__HEIGHT__))
pygame.display.set_caption("marIO")

import sprites
import world


class Game:
    def __init__(self):
        self.run = True
        self.w_height = config.__HEIGHT__
        self.w_width = config.__WIDTH__
        self.world = world.World((self.w_width, self.w_height))
        sprites.background = pygame.transform.scale(sprites.background, (self.w_width, self.w_height))

    def draw(self):
        win.blit(sprites.background, (0, 0))
        self.world.sprites.draw(win)

    def start(self):
        self.world.generate()
        while self.run:
            clock = pygame.time.Clock()
            clock.tick_busy_loop(6000)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False
                    print('exit')

            keys_list = pygame.key.get_pressed()
            actions = []
            if keys_list[pygame.K_a]:
                actions.append(world.ACTION_BACK)
            if keys_list[pygame.K_d]:
                actions.append(world.ACTION_FORWARD)
            if keys_list[pygame.K_SPACE]:
                actions.append(world.ACTION_JUMP)
            if actions:
                for _action in actions:
                    self.world.playerSubject.perform_action(_action)
            else:
                self.world.playerSubject.perform_action(world.ACTION_NONE)
            self.world.tick()
            self.draw()
            pygame.display.update()
        pygame.quit()


def main():
    game = Game()
    game.start()


if __name__ == '__main__':
    main()
