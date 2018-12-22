import random

import pygame
import config
import objects.agent
import objects.object
import sprites

ACTION_NONE = 0
ACTION_FORWARD = 1
ACTION_BACK = 2
ACTION_JUMP = 3


class World:
    def __init__(self, bounds):
        self.sprites = pygame.sprite.Group()
        self.subjects = pygame.sprite.Group()
        self.platforms = pygame.sprite.Group()
        self.lose_triggers = pygame.sprite.Group()
        self.bounds = bounds
        self.width, self.height = bounds
        self.view_x = 0
        self.block_length = 0

        player_x = 0
        player_y = self.height - config.__BLOCK_SIZE__ - config.__PLAYER_HEIGHT__
        self.playerSubject = objects.agent.PlayerAgent(
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

        self.ended = False
        self.score = 0

    def generate(self):
        self.block_length = random.randint(400, 1000)
        floor_x = 0
        floor_y = self.height - config.__BLOCK_SIZE__
        for i in range(self.block_length):
            block = objects.object.Block(floor_x, floor_y, config.__BLOCK_SIZE__, config.__BLOCK_SIZE__)
            self.platforms.add(block)
            self.sprites.add(block)
            if random.random() < 0.05:
                floor_x += 3 * config.__BLOCK_SIZE__
            else:
                floor_x += config.__BLOCK_SIZE__

        kill_block = objects.object.SimpleObject(
            0,
            self.height,
            self.block_length * config.__BLOCK_SIZE__,
            50,
        )
        self.lose_triggers.add(kill_block)

        # block = objects.object.Block(60, self.height - config.__BLOCK_SIZE__ - 50, config.__BLOCK_SIZE__,
        # config.__BLOCK_SIZE__)

        # self.objects.add(block)
        # self.sprites.add(block)

    def tick(self):
        for subject in self.subjects:
            subject.tick(self)
            subject.update()

        hits = pygame.sprite.spritecollide(self.playerSubject, self.lose_triggers, False)
        if hits:
            self.end()

        center_x = self.view_x + self.width / 2.0
        dx = self.playerSubject.rect.x - center_x
        if dx > 0:
            self.view_x += dx

    def end(self):
        self.ended = True

    def draw(self, win):
        for sprite in self.sprites:
            world_rect = pygame.Rect((self.view_x, 0, self.width, self.height))
            if sprite.rect.colliderect(world_rect):
                sprite.draw(win, self.view_x)

