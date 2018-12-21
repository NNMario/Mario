import pygame
import helpers
import world


class Agent(pygame.sprite.Sprite):
    def __init__(self, x: float, y: float, width: float, height: float, sprite=None):
        pygame.sprite.Sprite.__init__(self)
        self.image = sprite
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y

        self.velocity = helpers.Vec2d(0, 0)
        self.current_velocity = helpers.Vec2d(0, 0)
        self.acceleration = helpers.Vec2d(0, 0)
        self.is_jump = False
        self.jumpTicks = -10

        self._sprite = None
        self._type = None

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
            self.is_jump = True
            self.current_velocity.y = -1 * self.velocity.y
            # self.rect.x += 1
            # hits = pg.sprite.spritecollide(self, self.game.platforms, False)
            # self.rect.x -= 1

    def stop_jump(self):
        self.is_jump = False

    def move(self, world):
        self.current_velocity += self.acceleration
        dx = self.current_velocity.x + 0.5 * self.acceleration.x
        self.rect.x += dx

        w_width, w_height = world.bounds
        if self.rect.x + self.rect.width > w_width and self.current_velocity.x > 0:
            self.rect.x = w_width - self.rect.width
            self.current_velocity.x = 0
        elif self.rect.x <= 0 and self.current_velocity.x < 0:
            self.current_velocity.x = 0
            self.rect.x = 0

        hits = pygame.sprite.spritecollide(self, world.sprites, False)
        for hit in hits:
            if hit != self:
                if dx > 0:
                    self.rect.right = hit.rect.left
                    self.current_velocity.x = 0
                else:
                    self.rect.left = hit.rect.right
                    self.current_velocity.x = 0

        dy = self.current_velocity.y + 0.5 * self.acceleration.y
        self.rect.y += dy
        if self.rect.y + self.rect.height > w_height and self.current_velocity.y < 0:
            self.rect.y = w_height - self.rect.height
            self.current_velocity.y = 0
        elif self.rect.y < 0 and self.current_velocity.y > 0:
            self.current_velocity.y = 0
            self.rect.y = 0

        hits = pygame.sprite.spritecollide(self, world.sprites, False)
        for hit in hits:
            if hit != self:
                if dy > 0:
                    self.rect.bottom = hit.rect.top
                    self.current_velocity.y = 0
                    self.stop_jump()
                else:
                    self.rect.top = hit.rect.bottom
                    self.current_velocity.y = 0



class PlayerAgent(Agent):
    def __init__(self, x: float, y: float, width: float, height: float, sprite=None):
        Agent.__init__(self, x, y, width, height, sprite)
        self._type = 'Player'
