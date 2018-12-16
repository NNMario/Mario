import pygame
import world
import config
import helpers


class Agent(pygame.sprite.Sprite):
    def __init__(self, x: float, y: float, width: float, height: float, sprite=None):
        pygame.sprite.Sprite.__init__(self)
        self.image = sprite
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect()
        self.rect.topleft = x, y

        self.position = helpers.Vec2d(x, y)
        self.velocity = helpers.Vec2d(0, 0)
        self.current_velocity = helpers.Vec2d(0, 0)
        self.acceleration = helpers.Vec2d(0, 0)
        self.is_jump = False
        self.jumpTicks = -10

        self._sprite = None
        self._type = None

    def update(self):
        self.rect.topleft = self.position.x, self.position.y

    def perform_action(self, action):
        if action == world.ACTION_NONE:
            self.current_velocity.x = 0
            self.acceleration.x = 0
        elif action == world.ACTION_BACK:
            self.current_velocity.x = self.velocity.x * -1
        elif action == world.ACTION_FORWARD:
            self.current_velocity.x = self.velocity.x
        elif action == world.ACTION_JUMP:
            self.jump()

    def set_velocity(self, vx, vy):
        self.velocity = helpers.Vec2d(vx, vy)

    def set_acceleration(self, ax, ay):
        self.acceleration = helpers.Vec2d(ax, ay)

    def jump(self):
        if not self.is_jump:
            self.acceleration.y = config.__GRAVITY__
            self.is_jump = True
            self.current_velocity.y = -1 * self.velocity.y
            # self.rect.x += 1
            # hits = pg.sprite.spritecollide(self, self.game.platforms, False)
            # self.rect.x -= 1

    def stop_jump(self):
        self.is_jump = False
        self.current_velocity.y = 0
        self.acceleration.y = 0

    def move(self):
        self.current_velocity += self.acceleration
        self.position += self.current_velocity + 0.5 * self.acceleration


class PlayerAgent(Agent):
    def __init__(self, x: float, y: float, width: float, height: float, sprite=None):
        Agent.__init__(self, x, y, width, height, sprite)
        self._type = 'Player'
