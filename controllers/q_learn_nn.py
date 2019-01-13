import math
import pickle
import random
from collections import deque
from keras import regularizers
import numpy as np
from keras.layers import Dense, Activation
from keras.layers import Dropout
from keras.models import Sequential
from keras.models import model_from_json

import environment
from controllers.controller import Controller


def distance(obj1, obj2):
    return math.sqrt((obj1.x - obj2.x) ** 2 + (obj2.y - obj2.y) ** 2)


def closest_item(player_rect, items):
    closest = None
    closest_dist = None
    for item in items:
        if item.x >= player_rect.x:
            dist = distance(item, player_rect)
            if closest is None or dist < closest_dist:
                closest = item
                closest_dist = dist

    return closest, closest_dist


class DeepQLearning(Controller):
    def __init__(self, actions, epsilon=1.0, alpha=0.001, gamma=0.9):
        Controller.__init__(self)
        self.epsilon = epsilon
        self.alpha_decay = 0.995
        self.min_alpha = 0.0001
        self.epsilon_minimum = 0.001
        self.alpha = alpha
        self.gamma = gamma
        self.batch_size = 32
        self.world = environment
        self.actions = actions

        self.last_action = environment.ACTION_NONE
        self.last_state = None
        self.old_x = None
        self.old_y = None
        self.last_acc = None

        self.state_len = 28
        self.model = Sequential([
            Dense(100, input_shape=(self.state_len,)),
            Activation('relu'),
            Dense(150, kernel_regularizer=regularizers.l2(0.01), activity_regularizer=regularizers.l1(0.01)),
            Activation('relu'),
            Dropout(0.1),
            Dense(70, kernel_regularizer=regularizers.l2(0.01), activity_regularizer=regularizers.l1(0.01)),
            Activation('relu'),
            # Dense(800, input_shape=(self.state_len,)),
            Dense(len(self.actions)),
            Activation('linear')
        ])
        self.event_buffer = deque(maxlen=2048)
        self.model.compile(optimizer='adam', loss='mean_squared_error', metrics=['accuracy'])
        self.episode_nr = 0
        # fig = plt.figure()
        # plt.axis([0, 1000, 0, 1])
        # plt.show()

    def save(self):
        with open('model.data', 'w') as export_to:
            export_to.write(self.model.to_json())
        self.model.save_weights(filepath='model.weights')
        with open('model.variables', 'wb') as export_vars:
            data = [self.gamma, self.alpha, self.epsilon, self.batch_size]
            pickle.dump(data, export_vars)

    def load(self):
        with open('model.data') as mf:
            self.model = model_from_json(mf.read())
            self.model.compile(optimizer='adam', loss='mean_squared_error', metrics=['accuracy'])

        self.model.load_weights('model.weights')
        self.model._make_predict_function()

        with open('model.variables', 'rb') as import_vars:
            self.gamma, self.alpha, self.epsilon, self.batch_size = pickle.load(import_vars)

    def gap_info(self, env):
        closest = None
        closest_dist = None

        first = 0
        second = 0
        third = 0
        passed = 0
        for gap in env.gaps:
            if gap.x >= env.player_agent.rect.x:
                dist = distance(gap, env.player_agent.rect)
                if closest is None or dist < closest_dist:
                    closest = gap
                    closest_dist = dist
            if env.player_agent.first_rect.colliderect(gap):
                first, second, third = 1, 1, 1
            elif env.player_agent.second_rect.colliderect(gap):
                second, third = 1, 1
            elif env.player_agent.third_rect.colliderect(gap):
                third = 1

            if 20 > env.player_agent.rect.x - gap.right > 0 and not env.ended:
                passed = 1

        dx = 200
        dy = 200

        if closest is None:# or closest_dist > 200:
            closest_dist = 200
            dx = 200
            dy = 200
        else:
            dx = env.player_agent.rect.x - closest.x
            dy = env.player_agent.rect.y - closest.y

        return closest_dist, dx, dy, first, second, third, passed


    def upper_platform(self, env):
        closest, closest_dist = closest_item(env.player_agent.rect, env.upper_platforms)
        if not closest:# or closest_dist > 200:
            dx = 200
            dy = 200
            dist = 200
            height = 50
        else:
            dx = env.player_agent.rect.x - closest.x
            dy = env.player_agent.rect.y - closest.y
            dist = closest_dist
            height = closest.bottom - env.ground_height
        return dx, dy, dist, height

    def nearest_coin(self, env):
        closest, closest_dist = closest_item(env.player_agent.rect, env.coins)
        if not closest:# or closest_dist > 200:
            dx = 200
            dy = 200
            dist = 200
        else:
            dx = env.player_agent.rect.x - closest.x
            dy = env.player_agent.rect.y - closest.y
            dist = closest_dist
        return dx, dy, dist

    def nearest_tube(self, env):
        closest, closest_dist = closest_item(env.player_agent.rect, env.tubes)
        if not closest:# or closest_dist > 200:
            dx = 200
            dy = 200
            dist = 200
            height = 50
        else:
            dx = env.player_agent.rect.x - closest.x
            dy = env.player_agent.rect.y - closest.y
            dist = closest_dist
            height = closest.height
        return dx, dy, dist, height

    def nearest_enemy(self, env):
        closest = None
        closest_dist = None
        for enemy in env.enemies:
            if enemy.rect.x > env.player_agent.rect.x:
                dist = distance(enemy.rect, env.player_agent.rect)
                if closest is None or dist < closest_dist:
                    closest = enemy
                    closest_dist = dist
        if closest is None:# or closest_dist > 200:
            return 200, 200, 0, 0, 200
        dx = env.player_agent.rect.x - closest.rect.x
        dy = env.player_agent.rect.y - closest.rect.y
        vx, vy = closest.current_velocity.x, closest.current_velocity.y
        return dx, dy, vx, vy, closest_dist

    def reward(self, env: environment.Environment, old_env: environment.Environment):
        dx = env.player_agent.rect.x - old_env.player_agent.rect.x
        state = self.get_state(env)
        score = 0
        if dx > 0:
            score += 100

        if env.player_agent.current_velocity.x == 0 and env.player_agent.current_velocity.y == 0:
            score -= 200

        if state[6]:
            score += 200

        #if env.player_agent.current_velocity.y == 0 and env.player_agent.rect.bottom != env.ground_height:
        #    score += 100

        if env.got_coin:
            score += 500
        # score += 10 * self.passed_gaps(env)
        if env.killed_enemy:
            score += 1000

        if env.ended and not env.is_win:
            score -= 5000
        elif env.ended and env.is_win:
            score += 10000
        return score

    def getQ(self, state):
        result = self.model.predict(state.reshape((1, -1)))
        return result[0]

    def learn(self):
        #if len(self.event_buffer) > self.batch_size:
        if True:
            # batch = random.sample(self.event_buffer, self.batch_size)
            temp_buffer = []
            nn_input = []
            nn_output = []
            for state1, action, reward, state2 in self.event_buffer:
                max_q_for_state_2 = np.amax(self.getQ(state2))
                target = reward + self.gamma * max_q_for_state_2
                q_for_state_1 = self.getQ(state1)
                q_for_state_1[action] = target
                td_error = abs(reward - q_for_state_1[action])
                # temp_buffer.append((state1, q_for_state_1, td_error))
                nn_input.append(state1)
                nn_output.append(q_for_state_1)

            # temp_buffer.sort(key=lambda x: x[2], reverse=True)
            # temp_buffer = temp_buffer[: len(temp_buffer) // 2]
            # nn_input, nn_output, _ = zip(*temp_buffer)
            history = self.model.fit(np.array(nn_input), np.array(nn_output), verbose=0, shuffle=True, batch_size=self.batch_size)
            self.last_acc = history.history['acc']
            print(self.epsilon)
            # print('ploting!')
            # plt.plot(self.episode_nr, history.history['acc'])

        if self.epsilon > self.epsilon_minimum:
            # self.epsilon *= self.epsilon_decay
            self.epsilon -= 0.03
        else:
            self.epsilon = self.epsilon_minimum

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

    def get_state(self, env: environment.Environment):
        state = np.array([
            0,  # 0 Player direction
            0,  # 1 Stuck? Doesn't move over several frames
            0,  # 2 On ground?
            0,  # 3 Is Jumping
            0,  # 4 Last action

            0,  # 5 Distance to closest gap
            0,  # 6 Passed gap?
            0,  # 7 Gap inside first rect
            0,  # 8 Gap inside second rect
            0,  # 9 Gap inside third rect
            0,  # 10 Gap dx
            0,  # 11 Gap dy

            0,  # 12 Player vx
            0,  # 13 Player vy
            0,  # 14 Player h above the ground

            0,  # 15 Distance to the closest upper platform
            0,  # 16 DX to the closest upper platform
            0,  # 17 DY to the closest upper platform
            0,  # 18 Upper platform height

            0,  # 19 DX to coin
            0,  # 20 DY to coin
            0,  # 21 Distance to coin

            0,  # 22 DX to tube
            0,  # 23 DY to tube
            0,  # 24 Distance to tube
            0,  # 25 Tube height

            0,  # 26 DX to enemy
            0,  # 27 DY to enemy
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

        closest_dist, dx, dy, first, second, third, passed = self.gap_info(env)
        state[5] = closest_dist
        state[6] = passed
        state[10] = dx
        state[11] = dy

        state[12] = player.current_velocity.x
        state[13] = player.current_velocity.y
        state[14] = player.rect.bottom - env.ground_height

        dx, dy, dist, height = self.upper_platform(env)
        state[15] = dist
        state[16] = dx
        state[17] = dy
        state[18] = height

        state[19], state[20], state[21] = self.nearest_coin(env)
        state[22], state[23], state[24], state[25] = self.nearest_tube(env)
        state[26], state[27], state[7], state[8], state[9] = self.nearest_enemy(env)

        return state
