import math
import random
from collections import deque
import numpy as np
from keras.layers import Dense, Activation
from keras.models import Sequential
from keras import initializers
import environment
from controllers.controller import Controller
import config
import matplotlib.pyplot as plt


def distance(obj1, obj2):
    return math.sqrt((obj1.x - obj2.x) ** 2 + (obj2.y - obj2.y) ** 2)


class DeepQLearning(Controller):
    def __init__(self, actions, epsilon=1.0, alpha=0.001, gamma=0.9):
        Controller.__init__(self)
        self.epsilon = epsilon
        self.alpha_decay = 0.995
        self.min_alpha = 0.0001
        self.epsilon_minimum = 0.01
        self.alpha = alpha
        self.gamma = gamma
        self.batch_size = 1000
        self.world = environment
        self.actions = actions

        self.last_action = environment.ACTION_NONE
        self.last_state = None
        self.old_x = None
        self.old_y = None

        self.state_len = 17
        self.model = Sequential([
            Dense(130, input_shape=(self.state_len,)),
            Activation('relu'),
            Dense(len(self.actions)),
            Activation('linear')
        ])
        self.event_buffer = deque(maxlen=10000)
        self.model.compile(optimizer='rmsprop', loss='mse', metrics=['accuracy'])
        self.episode_nr = 0
        # fig = plt.figure()
        # plt.axis([0, 1000, 0, 1])
        # plt.show()

    def passed_gaps(self, env):
        for gap in env.gaps:
            if 20 > env.player_agent.rect.x - gap.right > 0 and not env.ended:
                return True
        return False

    def got_coin(self, env):
        for coin in env.coins:
            if env.player_agent.rect.colliderect(coin): return True
        return False

    def upper_platform(self, env):
        closest = None
        closest_dist = None
        for upper in env.upper_platforms:
            if upper.x > env.player_agent.rect.x:
                dist = distance(upper, env.player_agent.rect)
                if closest is None or dist < closest_dist:
                    closest = upper
                    closest_dist = dist
        if closest is None or closest_dist > 200:
            return 200, (0, 0)
        else:
            return closest_dist, (env.player_agent.rect.x - closest.x, env.player_agent.rect.y - closest.y)

    def reward(self, env: environment.Environment, old_env: environment.Environment):
        dx = env.player_agent.rect.x - old_env.player_agent.rect.x
        score = 0
        score += env.player_agent.rect.x / 10
        if env.player_agent.current_velocity.x == 0 and env.player_agent.current_velocity.y == 0:
            score -= 200
        if self.passed_gaps(env):
            score += 100

        if env.got_coin:
            score += 1000
        # score += 10 * self.passed_gaps(env)

        if env.ended and not env.is_win:
            score -= 5000
        elif env.ended and env.is_win:
            score += 5000
        return score

    def getQ(self, state):
        result = self.model.predict(state.reshape((1, -1)))
        return result[0]

    def learn(self):
        if len(self.event_buffer) > self.batch_size:
            batch = random.sample(self.event_buffer, self.batch_size)
            nn_input = []
            nn_output = []
            for state1, action, reward, state2 in batch:
                max_q_for_state_2 = np.amax(self.getQ(state2))
                target = reward + self.gamma * max_q_for_state_2
                q_for_state_1 = self.getQ(state1)
                q_for_state_1[action] = target
                nn_input.append(state1)
                nn_output.append(q_for_state_1)
                print(state1)
            history = self.model.fit(np.array(nn_input), np.array(nn_output), verbose=0, shuffle=True)
            print(history.history['acc'], history.history['loss'])
            # print('ploting!')
            # plt.plot(self.episode_nr, history.history['acc'])

        if self.epsilon > self.epsilon_minimum:
            # self.epsilon *= self.epsilon_decay
            self.epsilon -= 0.01
        #if self.alpha > self.min_alpha:
        #    self.alpha *= self.alpha_decay

        print('Learning process ended!')

    def remember(self, env: environment.Environment, action, reward: int, next_env: environment.Environment):
        state = self.get_state(env)
        next_state = self.get_state(next_env)
        self.event_buffer.append((state, action, reward, next_state))

    def get_action(self, env: environment.Environment):
        state = self.get_state(env)
        if random.random() < self.epsilon:
            action = random.choice(self.actions)
        else:
            results = self.getQ(state)
            max_action = np.argwhere(results == np.amax(results))
            max_action = max_action.flatten().tolist()
            action = self.actions[random.choice(max_action)]
        self.last_action = action
        return action

    def done(self, episode_nr=0):
        self.episode_nr = episode_nr
        self.learn()
        print(self.epsilon)
        print(self.alpha)

    def get_state(self, env: environment.Environment):
        state = np.array([
            0,  # 0 Player direction
            0,  # 1 Stuck? Doesn't move over several frames
            0,  # 2 On ground?
            0,  # 3 Is Jumping
            0,  # 4 Last action
            0,  # 5 Has gaps nearby (distance)
            0,  # 6 Passed gap?
            0,  # 7 Gap inside first rect
            0,  # 8 Gap inside second rect
            0,  # 9 Gap inside third rect
            0,  # 10 Player vx
            0,  # 11 Player vy
            0,  # 12 Distance to the closest upper platform
            0,  # 13 DX to the closest upper platform
            0,  # 14 DY to the closest upper platform
            0,  # 15 DX to the closest gap
            0,  # 16 DY to the closest gap
        ])

        player = env.player_agent
        if player.current_velocity.x > 0 and player.current_velocity.y < 0:
            state[0] = 1
        elif player.current_velocity.x > 0 and player.current_velocity.y == 0:
            state[0] = 2
        elif player.current_velocity.x > 0 and player.current_velocity.y > 0:
            state[0] = 3
        elif player.current_velocity.x == 0 and player.current_velocity.y > 0:
            state[0] = 4
        elif player.current_velocity.x == 0 and player.current_velocity.y < 0:
            state[0] = 0
        elif player.current_velocity.x == 0 and player.current_velocity.y == 0:
            state[0] = 8
        elif player.current_velocity.x < 0 and player.current_velocity.y > 0:
            state[0] = 5
        elif player.current_velocity.x < 0 and player.current_velocity.y < 0:
            state[0] = 7
        elif player.current_velocity.x < 0 and player.current_velocity.y == 0:
            state[0] = 6

        if player.old_x == player.rect.x and player.old_y == player.rect.y:
            state[1] = 1
        if player.rect.y == env.ground_height - player.rect.height:
            state[2] = 1
        state[3] = player.is_jump
        state[4] = self.last_action

        collide_rect = player.rect.copy()
        collide_rect.width += 10
        collide_rect.height += 1
        state[5] = 100

        closest_gap = None
        closest_dist = 200
        for gap in env.gaps:
            # state[5] = min(state[5], distance(agent, gap))
            if collide_rect.x < gap.x:
                dist = distance(player.rect, gap)
                if closest_gap is None or dist < closest_dist:
                    closest_dist = dist
                    closest_gap = gap
            if gap.colliderect(player.first_rect):
                state[7] = 1
                state[8] = 1
                state[9] = 1
            elif gap.colliderect(player.second_rect):
                state[8] = 1
                state[9] = 1
            elif gap.colliderect(player.third_rect):
                state[9] = 1

        state[5] = closest_dist
        state[6] = 1 if self.passed_gaps(env) else 0
        state[10] = player.current_velocity.x
        state[11] = player.current_velocity.y
        dist, angle = self.upper_platform(env)
        state[12] = min(200.0, dist)
        state[13], state[14] = angle
        if closest_gap is not None:
            state[15] = env.player_agent.rect.x - closest_gap.x
            state[16] = env.player_agent.rect.y - closest_gap.y
        else:
            state[15], state[16] = 200, 200
        # print(state)
        return state
