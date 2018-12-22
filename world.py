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
        self.max_x = 0
        self.coins = 0
        self.score = 0

    def generate(self):
        self.block_length = 100  # random.randint(400, 1000)

        # Add the floor platforms
        floor_x = 0
        floor_y = self.height - config.__BLOCK_SIZE__
        for i in range(self.block_length):
            block = objects.object.Block(floor_x, floor_y, config.__BLOCK_SIZE__, config.__BLOCK_SIZE__)
            self.platforms.add(block)
            self.sprites.add(block)
            if random.random() < 0.1:
                floor_x += 3 * config.__BLOCK_SIZE__
            else:
                floor_x += config.__BLOCK_SIZE__

        # Add sprites that make the player lose on collision
        kill_block = objects.object.SimpleObject(
            0,
            self.height,
            self.block_length * config.__BLOCK_SIZE__,
            50,
        )
        self.lose_triggers.add(kill_block)

        princess = objects.object.Drawable(
            (self.block_length - 10) * config.__BLOCK_SIZE__,
            floor_y - config.__PRINCESS_HEIGHT__,
            config.__PRINCESS_WIDTH__,
            config.__PRINCESS_HEIGHT__,
            sprites.princess
        )
        self.sprites.add(princess)

    def tick(self):
        for subject in self.subjects:
            subject.tick(self)
            subject.update()

        hits = pygame.sprite.spritecollide(self.playerSubject, self.lose_triggers, False)
        if hits:
            self.end()
            return

        center_x = self.view_x + self.width / 2.0
        dx = self.playerSubject.rect.x - center_x
        if dx > 0 and self.view_x + self.width < self.block_length * config.__BLOCK_SIZE__:
            self.view_x += dx

        self.calculate_score()

    def end(self):
        self.ended = True

    def calculate_score(self):
        self.max_x = max(self.max_x, self.playerSubject.rect.x)
        self.score = self.max_x + self.coins

    def draw(self, win):
        for sprite in self.sprites:
            world_rect = pygame.Rect((self.view_x, 0, self.width, self.height))
            if sprite.rect.colliderect(world_rect):
                sprite.draw(win, self.view_x)
