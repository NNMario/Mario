import pygame
import config
import subjects.agent
import objects.object
import sprites
import helpers

ACTION_NONE = 0
ACTION_FORWARD = 1
ACTION_BACK = 2
ACTION_JUMP = 3


class World:
    def __init__(self, bounds):
        self.sprites = pygame.sprite.Group()
        self.objects = pygame.sprite.Group()
        self.subjects = pygame.sprite.Group()
        self.bounds = bounds
        self.width, self.height = bounds

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

        self.subjects.add(self.playerSubject)
        self.sprites.add(self.playerSubject)

    def generate(self):
        width, height = self.bounds
        for i in range(0, width, config.__BLOCK_SIZE__):
            x = i
            y = self.height - config.__BLOCK_SIZE__
            block = objects.object.Block(x, y, config.__BLOCK_SIZE__, config.__BLOCK_SIZE__)
            self.objects.add(block)
            self.sprites.add(block)

    def tick(self):
        for subject in self.subjects:
            subject.move()
            self.check_move(subject)
            subject.update()

    def check_move(self, subject):
        w_width, w_height = self.bounds
        if subject.position.x + subject.rect.width > w_width:
            subject.position.x = w_width - subject.rect.width
        elif subject.position.x < 0:
            subject.position.x = 0
        elif subject.position.y + subject.rect.height > w_height:
            subject.position.y = w_height - subject.rect.height
        elif subject.position.y < 0:
            subject.position.y = 0

        hits = pygame.sprite.spritecollide(subject, self.sprites, False)

        for hit in hits:
            if hit != subject and subject.current_velocity.y > 0:
                subject.position.y = hit.rect.y - subject.rect.height
                subject.stop_jump()
                break
