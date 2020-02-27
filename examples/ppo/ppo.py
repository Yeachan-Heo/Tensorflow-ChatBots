from tensorflow.keras import *

import gym
import tensorflow as tf

class PPO(object):
    def __init__(self, **kwargs):
        self._env = None

    def set_env(self, env: gym.Env or str) -> None:
        self._env = env \
            if isinstance(env, gym.Env) \
            else gym.make(env)
        return None

