from controllers.controller import Controller
import random
import numpy as np
import world
from keras.layers import Dense, Activation
from keras.models import Sequential
from agents.agent import Agent
from collections import deque
import config
import pygame
from copy import deepcopy
import time
import math

ACTION_LEFT_JUMP = 0
ACTION_LEFT_NO_JUMP = 1
ACTION_RIGHT_JUMP = 2
ACTION_RIGHT_NO_JUMP = 3
ACTION_STAY_JUMP = 4
ACTION_STAY_NO_JUMP = 5


def distance(obj1, obj2):
    return math.sqrt((obj1.rect.x - obj2.rect.x) ** 2 + (obj2.rect.y - obj2.rect.y) ** 2)


class DeepQLearning(Controller):
    def __init__(self, actions, epsilon=1.0, alpha=0.2, gamma=0.9):
        Controller.__init__(self)
        self.epsilon = epsilon
        self.epsilon_decay = 0.955
        self.epsilon_minimum = 0.01
        self.alpha = alpha
        self.gamma = gamma
        self.batch_size = 32
        self.world = world
        self.actions = actions
        self.nn_actions = [
            ACTION_RIGHT_JUMP,
            ACTION_RIGHT_NO_JUMP,
            ACTION_LEFT_JUMP,
            ACTION_LEFT_NO_JUMP
        ]

        self.last_action = world.ACTION_NONE
        self.last_state = None
        self.old_x = None
        self.old_y = None

        self.state_len = 7
        self.model = Sequential([
            Dense(50, input_shape=(self.state_len,)),
            Activation('relu'),
            Dense(len(self.nn_actions)),
            Activation('linear')
        ])
        self.event_buffer = deque(maxlen=100000)
        self.model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

    def passed_gap(self, agent, world_state):
        collide_rect = agent.rect.copy()
        collide_rect.x -= agent.rect.width - 10
        collide_rect.height += 1
        for gap in world_state.gaps:
            if collide_rect.colliderect(gap.rect):
                return distance(agent, gap)
        return 100

    def calculate_reward(self, agent, world_state):
        dx = agent.rect.x - self.old_x
        dy = agent.rect.y - self.old_y
        score = 0
        if dx > 0:
            score += 1
        else:
            score -= 2
        if self.passed_gap(agent, world_state):
            score += 5
        if world_state.ended and not world_state.win:
            score -= 100
        elif world_state.ended and world_state.win:
            score += 100
        return score

    def get_state(self, agent, world_state: world.World):
        state = np.array([
            0,  # 0 Player direction
            0,  # 1 Stuck? Doesn't move over several frames
            0,  # 2 On ground?
            0,  # 3 Is Jumping
            0,  # 4 Last action
            0,  # 5 Has gaps nearby
            0,  # 6 Passed gap?
        ])
        player = world_state.player_agent
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

        if self.old_x == agent.rect.x and self.old_y == agent.rect.y:
            state[1] = 1
        if agent.rect.y == world_state.ground_height - agent.rect.height:
            state[2] = 1
        state[3] = player.is_jump
        state[4] = self.last_action

        collide_rect = agent.rect.copy()
        collide_rect.width += 10
        collide_rect.height += 1
        # state[5] = 100
        for gap in world_state.gaps:
            # state[5] = min(state[5], distance(agent, gap))
            if collide_rect.colliderect(gap.rect) and collide_rect.x < gap.rect.x:
                state[5] = distance(agent, gap)
                break

        state[6] = self.passed_gap(agent, world_state)

        # platforms = np.array([self.distance(player, obj) for obj in world_state.platforms])
        # platforms.sort()
        return state

    def getQ(self, state):
        result = self.model.predict(state.reshape((1, -1)))
        return result[0]

    def learn(self):
        if len(self.event_buffer) > self.batch_size:
            batch = random.sample(self.event_buffer, self.batch_size)
            for state1, action, reward, state2 in batch:
                maxq_for_state_2 = np.amax(self.getQ(state2))
                target = reward + self.gamma * maxq_for_state_2
                q_for_state_1 = self.getQ(state1)
                q_for_state_1[action] = target
                self.model.fit(state1.reshape(1, -1), q_for_state_1.reshape(1, -1), verbose=0)

        if self.epsilon > self.epsilon_minimum:
            # self.epsilon *= self.epsilon_decay
            self.epsilon -= 0.01
        print('Learning process ended!')

    def get_actions(self, agent, world_state: world.World):
        action = ACTION_LEFT_JUMP
        state = self.get_state(agent, world_state)

        if random.random() < self.epsilon:
            action = random.choice(self.nn_actions)
        else:
            results = self.getQ(state)
            max_action = np.argwhere(results == np.amax(results))
            max_action = max_action.flatten().tolist()
            action = self.nn_actions[random.choice(max_action)]

        if self.last_state is not None:
            reward = self.calculate_reward(agent, world_state)
            self.event_buffer.append((self.last_state, self.last_action, reward, state))

        self.last_state = state
        self.last_action = action
        self.old_x = agent.rect.x
        self.old_y = agent.rect.y

        if action == ACTION_LEFT_JUMP:
            return [world.ACTION_JUMP, world.ACTION_FORWARD]
        elif action == ACTION_LEFT_NO_JUMP:
            return [world.ACTION_FORWARD]
        elif action == ACTION_RIGHT_JUMP:
            return [world.ACTION_JUMP, world.ACTION_BACK]
        elif action == ACTION_RIGHT_NO_JUMP:
            return [world.ACTION_BACK]
        elif action == ACTION_STAY_JUMP:
            return [world.ACTION_JUMP]
        elif action == ACTION_STAY_NO_JUMP:
            return [world.ACTION_NONE]

    def done(self):

        self.learn()
        print(self.epsilon)
        self.event_buffer.clear()
