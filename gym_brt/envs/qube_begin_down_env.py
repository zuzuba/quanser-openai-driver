from __future__ import absolute_import
from __future__ import print_function
from __future__ import division

import numpy as np
from gym import spaces
from gym_brt.envs.qube_base_env import \
    QubeBaseEnv, \
    normalize_angle, \
    ACTION_HIGH, \
    ACTION_LOW


class QubeBeginDownReward(object):
    def __init__(self):
        self.target_space = spaces.Box(
            low=ACTION_LOW,
            high=ACTION_HIGH, dtype=np.float32)

    def __call__(self, state, action):
        theta_x = state[0]
        theta_y = state[1]
        alpha_x = state[2]
        alpha_y = state[3]
        theta_velocity = state[4]
        alpha_velocity = state[5]
        theta_acceleration = state[6]
        alpha_acceleration = state[7]

        theta = np.arctan2(theta_y, theta_x)  # arm
        alpha = np.arctan2(alpha_y, alpha_x)  # pole

        cost = normalize_angle(theta)**4 + \
            normalize_angle(alpha)**2 + \
            0.1 * alpha_velocity**2

        reward = -cost
        return reward


class QubeBeginDownEnv(QubeBaseEnv):
    def __init__(self, frequency=1000, use_simulator=False):
        super(QubeBeginDownEnv, self).__init__(
            frequency=frequency,
            use_simulator=use_simulator)
        self.reward_fn = QubeBeginDownReward()


def main():
    num_episodes = 10
    num_steps = 250

    with QubeBeginDownEnv() as env:
        for episode in range(num_episodes):
            state = env.reset()
            for step in range(num_steps):
                action = env.action_space.sample()
                state, reward, done, _ = env.step(action)


if __name__ == '__main__':
    main()
