import pygame
import helpers
import environment
import objects.object
import numpy as np
import config

class Agent(objects.object.Drawable):
    def __init__(self, x, y, width, height):
        objects.object.Drawable.__init__(self, x, y, width, height)

        self._velocity = helpers.Vec2d(0, 0)
        self.current_velocity = helpers.Vec2d(0, 0)
        self.acceleration = helpers.Vec2d(0, 0)
        self.is_jump = False
        self._type = None
        self.first_rect = None
        self.second_rect = None
        self.third_rect = None
        self._update_rects()
        self.old_x = 0
        self.old_y = 0

    @property
    def position(self):
        return np.array([self.rect.x, self.rect.y])

    @property
    def velocity(self):
        return np.array([self.current_velocity.x, self.current_velocity.y])

    def perform_action(self, action):
        if action == environment.ACTION_NONE:
            self.current_velocity.x = 0
            self.acceleration.x = 0
        elif action == environment.ACTION_BACK:
            self.current_velocity.x = self._velocity.x * -1
        elif action == environment.ACTION_FORWARD:
            self.current_velocity.x = self._velocity.x
        elif action == environment.ACTION_JUMP:
            self._jump()

    def set_velocity(self, vx, vy):
        self._velocity = helpers.Vec2d(vx, vy)

    def set_acceleration(self, ax, ay):
        self.acceleration = helpers.Vec2d(ax, ay)

    def _jump(self):
        if not self.is_jump:
            self.is_jump = True
            self.current_velocity.y = -1 * self._velocity.y
            # self.rect.x += 1
            # hits = pg.sprite.spritecollide(self, self.game.platforms, False)
            # self.rect.x -= 1

    def _stop_jump(self):
        self.is_jump = False

    def _update_rects(self):
        self.first_rect = self.rect.copy()
        self.first_rect.width += config.__FIRST_RECT__
        self.first_rect.x -= config.__FIRST_RECT__ / 2
        self.first_rect.height += config.__FIRST_RECT__
        self.first_rect.y -= config.__FIRST_RECT__ / 2

        self.second_rect = self.rect.copy()
        self.second_rect.width += config.__SECOND_RECT__
        self.second_rect.x -= config.__SECOND_RECT__ / 2
        self.second_rect.height += config.__SECOND_RECT__
        self.second_rect.y -= config.__SECOND_RECT__ / 2

        self.third_rect = self.rect.copy()
        self.third_rect.width += config.__THIRD_RECT__
        self.third_rect.x -= config.__THIRD_RECT__ / 2
        self.third_rect.height += config.__THIRD_RECT__
        self.third_rect.y -= config.__THIRD_RECT__ / 2

    def tick(self, env):
        self.old_x = self.rect.x
        self.old_y = self.rect.y

        if self._type == 'Enemy':
            platforms = env.enemy_touchable
        else:
            platforms = env.platforms

        self.current_velocity += self.acceleration
        dx = self.current_velocity.x + 0.5 * self.acceleration.x
        self.rect.x += dx

        # Fix collisions
        if self.rect.x + self.rect.width > env.viewport_x + env.width and self.current_velocity.x > 0:
            self.rect.left = env.viewport_x + env.width - self.rect.width
            self.current_velocity.x = 0
        elif self.rect.x <= env.viewport_x and self.current_velocity.x < 0:
            self.current_velocity.x = 0
            self.rect.left = env.viewport_x

        for platform in platforms:
            if platform.colliderect(self.rect):
                if dx > 0:
                    self.rect.right = platform.left
                    self.current_velocity.x = 0
                else:
                    self.rect.left = platform.right
                    self.current_velocity.x = 0

        dy = self.current_velocity.y + 0.5 * self.acceleration.y
        self.rect.y += dy
        if self.rect.y + self.rect.height > env.height and self.current_velocity.y < 0:
            self.rect.y = env.height - self.rect.height
            self.current_velocity.y = 0
        elif self.rect.y < 0 and self.current_velocity.y > 0:
            self.current_velocity.y = 0
            self.rect.y = 0

        for platform in platforms:
            if platform.colliderect(self.rect):
                if dy > 0:
                    self.rect.bottom = platform.top
                    self.current_velocity.y = 0
                    self._stop_jump()
                else:
                    self.rect.top = platform.bottom
                    self.current_velocity.y = 0

        self._update_rects()