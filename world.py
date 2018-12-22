import random

import pygame
import config
import subjects.agent
import objects.object
import sprites

ACTION_NONE = 0
ACTION_FORWARD = 1
ACTION_BACK = 2
ACTION_JUMP = 3


class World:
    def __init__(self, bounds):
        self.sprites = pygame.sprite.Group()
        self.objects = pygame.sprite.Group()
        self.subjects = pygame.sprite.Group()
        self.platforms = pygame.sprite.Group()
        self.bounds = bounds
        self.width, self.height = bounds
        self.view_x = 0
        self.block_length = 0

        player_x = 0
        player_y = self.height - config.__BLOCK_SIZE__ - config.__PLAYER_HEIGHT__
        self.playerSubject = subjects.agent.PlayerAgent(
            player_x,
            player_y,
            config.__PLAYER_WIDTH__,
            config.__PLAYER_HEIGHT__,
            sprites.mario
        )
        self.playerSubject.set_velocity(3, 10)
        self.playerSubject.set_acceleration(0, config.__GRAVITY__)
        self.subjects.add(self.playerSubject)
        self.sprites.add(self.playerSubject)

    def generate(self):
        self.block_length = random.randint(400, 1000)
        floor_x = 0
        floor_y = self.height - config.__BLOCK_SIZE__
        for i in range(self.block_length):
            block = objects.object.Block(floor_x, floor_y, config.__BLOCK_SIZE__, config.__BLOCK_SIZE__)
            self.platforms.add(block)
            self.objects.add(block)
            self.sprites.add(block)
            if random.random() < 0.05:
                floor_x += 3 * config.__BLOCK_SIZE__
            else:
                floor_x += config.__BLOCK_SIZE__
        # block = objects.object.Block(60, self.height - config.__BLOCK_SIZE__ - 50, config.__BLOCK_SIZE__,
        # config.__BLOCK_SIZE__)

        # self.objects.add(block)
        # self.sprites.add(block)

    def tick(self):
        for subject in self.subjects:
            subject.tick(self)
            subject.update()
        center_x = self.view_x + self.width / 2.0
        dx = self.playerSubject.rect.x - center_x
        if dx > 0:
            self.view_x += dx

    def draw(self, win):
        for sprite in self.sprites:
            world_rect = pygame.Rect((self.view_x, 0, self.width, self.height))
            if sprite.rect.colliderect(world_rect):
                sprite.draw(win, self.view_x)

