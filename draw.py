import pygame
import environment
from graphics import sprites
import config


class Drawer:
    def __init__(self, width, height):
        pygame.init()
        pygame.font.init()
        self.win = pygame.display.set_mode((width, height))
        pygame.display.set_caption("marIO")
        self.w_height = height
        self.w_width = width
        # Create all the game sprites from the spritesheet
        sprites.setup()
        sprites.background = pygame.transform.scale(sprites.background, (self.w_width, self.w_height))
        sprites.block = pygame.transform.scale(sprites.block, (config.__BLOCK_SIZE__, config.__BLOCK_SIZE__))
        sprites.princess = pygame.transform.scale(sprites.princess,
                                                  (config.__PRINCESS_WIDTH__, config.__PRINCESS_HEIGHT__))
        for index, sprite in enumerate(sprites.mario):
            sprites.mario[index] = pygame.transform.scale(sprite, (config.__PLAYER_WIDTH__, config.__PLAYER_HEIGHT__))
        for index, sprite in enumerate(sprites.enemy):
            sprites.enemy[index] = pygame.transform.scale(sprite, (config.__BLOCK_SIZE__, config.__BLOCK_SIZE__))

        # The position of the viewport in the game map

    def draw_rect(self, rect, env, color, width=0):
        cp = rect.copy()
        cp.x -= env.viewport_x
        pygame.draw.rect(self.win, color, cp, width)

    def draw_texture(self, rect, env, sprite):
        cp = rect.copy()
        cp.x -= env.viewport_x
        self.win.blit(sprite, (cp.x, cp.y))

    def put_text(self, text, pos):
        myfont = pygame.font.SysFont('Comic Sans MS', 16)
        textsurface = myfont.render(text, False, (105,105,105))
        self.win.blit(textsurface, pos)

    def draw(self, env: environment.Environment, controller=None):
        self.win.blit(sprites.background, (0, 0))
        world_rect = pygame.Rect((env.viewport_x, 0, self.w_width, self.w_height))

        if config.__TEXTURES__:
            for platform in env.platforms:
                if world_rect.colliderect(platform):
                    self.draw_texture(platform, env, sprites.block)

            self.draw_texture(env.player_agent.rect, env, sprites.mario[(env.ticks // 20) % len(sprites.mario)])

            if world_rect.colliderect(env.princess):
                self.draw_texture(env.princess, env, sprites.princess)

            for coin in env.coins:
                if world_rect.colliderect(coin):
                    self.draw_texture(coin, env, sprites.coin[(env.ticks // 7) % len(sprites.coin)])

            for enemy in env.enemies:
                if world_rect.colliderect(enemy.rect):
                    self.draw_texture(enemy.rect, env, sprites.enemy[(env.ticks // 7) % len(sprites.enemy)])

            for tube in env.tubes:
                if world_rect.colliderect(tube):
                    sprite = pygame.transform.scale(sprites.tube, (tube.width, tube.height + config.__BLOCK_SIZE__ + 5))
                    self.draw_texture(tube, env, sprite)
            # self.draw_rect(env.player_agent.first_rect, env, (34, 139, 34), 2)
            # self.draw_rect(env.player_agent.second_rect, env, (32, 178, 170), 2)
            # self.draw_rect(env.player_agent.third_rect, env, (124, 252, 0), 1)
        else:
            # Draw the platforms
            for platform in env.platforms:
                if world_rect.colliderect(platform):
                    self.draw_rect(platform, env, (200, 200, 200))

            for gap in env.gaps:
                if world_rect.colliderect(gap):
                    self.draw_rect(gap, env, (135, 206, 235))
            # Draw the player
            self.draw_rect(env.player_agent.rect, env, (100, 100, 100))
            self.draw_rect(env.player_agent.first_rect, env, (34, 139, 34), 2)
            self.draw_rect(env.player_agent.second_rect, env, (32, 178, 170), 2)
            self.draw_rect(env.player_agent.third_rect, env, (124, 252, 0), 1)

            self.draw_rect(env.princess, env, (200, 0, 0), 2)

            for coin in env.coins:
                self.draw_rect(coin, env, (255, 255, 153))

            for enemy in env.enemies:
                if world_rect.colliderect(enemy.rect):
                    self.draw_rect(enemy.rect, env, (255, 0, 0))
                # self.draw_rect(enemy.top_rect, env.viewport_x, (255, 255, 0))

            for tube in env.tubes:
                if world_rect.colliderect(tube):
                    self.draw_rect(tube, env, (0, 200, 0))

        myfont = pygame.font.SysFont('Comic Sans MS', 30)
        textsurface = myfont.render(str(env.score), False, (255, 255, 255))
        self.win.blit(textsurface, (10, 5))
        if controller != None:
            state = controller.get_state(env)
            for index, val in enumerate(state):
                if index < len(state) / 2:
                    self.put_text('%d: %.1f' % (index, val), (self.w_width - 150, 14 * index))
                else:
                    self.put_text('%d: %.1f' % (index, val), (self.w_width - 70, 14 * (index - len(state) / 2 )))
        pygame.display.update()

    def uninit(self):
        pygame.quit()
