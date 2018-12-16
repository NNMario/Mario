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
            clock.tick_busy_loop(30)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False
                    print('exit')

            keys_list = pygame.key.get_pressed()
            action = world.ACTION_NONE
            if keys_list[pygame.K_a]:
                action = world.ACTION_BACK
            if keys_list[pygame.K_d]:
                action = world.ACTION_FORWARD
            if keys_list[pygame.K_SPACE]:
                action = world.ACTION_JUMP
            self.world.playerSubject.perform_action(action)

            self.world.tick()
            self.draw()
            pygame.display.update()
        pygame.quit()


def main():
    game = Game()
    game.start()


if __name__ == '__main__':
    main()
