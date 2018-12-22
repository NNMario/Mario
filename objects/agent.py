import pygame
import helpers
import world
import objects.object


class Agent(objects.object.Drawable):
    def __init__(self, x, y, width, height, sprite=None):
        objects.object.Drawable.__init__(self, x, y, width, height, sprite)

        self.velocity = helpers.Vec2d(0, 0)
        self.current_velocity = helpers.Vec2d(0, 0)
        self.acceleration = helpers.Vec2d(0, 0)
        self.is_jump = False
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
            self._jump()

    def set_velocity(self, vx, vy):
        self.velocity = helpers.Vec2d(vx, vy)

    def set_acceleration(self, ax, ay):
        self.acceleration = helpers.Vec2d(ax, ay)

    def _jump(self):
        if not self.is_jump:
            self.is_jump = True
            self.current_velocity.y = -1 * self.velocity.y
            # self.rect.x += 1
            # hits = pg.sprite.spritecollide(self, self.game.platforms, False)
            # self.rect.x -= 1

    def _stop_jump(self):
        self.is_jump = False

    def tick(self, world):
        self.current_velocity += self.acceleration
        dx = self.current_velocity.x + 0.5 * self.acceleration.x
        self.rect.x += dx

        # Fix collisions
        w_width, w_height = world.bounds
        if self.rect.x + self.rect.width > world.view_x + world.width and self.current_velocity.x > 0:
            self.rect.left = world.view_x + world.width - self.rect.width
            self.current_velocity.x = 0
        elif self.rect.x <= world.view_x and self.current_velocity.x < 0:
            self.current_velocity.x = 0
            self.rect.left = world.view_x

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
                    self._stop_jump()
                else:
                    self.rect.top = hit.rect.bottom
                    self.current_velocity.y = 0

    def draw(self, win, view_x=0):
        new_rect = self.rect.copy()
        new_rect.x -= view_x
        win.blit(self.image, new_rect)


class PlayerAgent(Agent):
    def __init__(self, x: float, y: float, width: float, height: float, sprite=None):
        Agent.__init__(self, x, y, width, height, sprite)
        self._type = 'Player'
