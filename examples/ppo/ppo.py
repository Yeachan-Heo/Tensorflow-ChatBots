from examples.ppo.utils import get_prob
from tensorflow_chatbots.variableholder.variableholder import VariableHolder
from tensorflow_chatbots.ttb.callback import TelegramBotCallback
from tensorflow.keras import *
from utils import *
from train import *
import random
import psutil
import numpy as np
import gym
import os


class PPO(object):
    def __init__(self, **kwargs):
        self._env = None
        self._vh = VariableHolder(**kwargs)
        self._policy_net = self._build_policy_net()
        self._value_net = self._build_value_net()
        if os.path.exists("./save_model/policy_net.h5"):
            self._policy_net = models.load_model("./save_model/policy_net.h5")
        if os.path.exists("./save_model/value_net.h5"):
            self._value_net = models.load_model("./save_model/value_net.h5")
        self._bot = TelegramBotCallback(token=self._vh.token)
        self._bot.set_variable_holder(self._vh)
        self.optimizer = optimizers.Adam
        self.episode_timer = Timer()
        self.train_timer = Timer()
    def set_env(self, env: gym.Env or str):
        self._env = env \
            if isinstance(env, gym.Env) \
            else gym.make(env)

    def _build_policy_net(self):
        state = layers.Input(shape=(self._vh.state_size,))
        h1 = layers.Dense(32, activation="relu")(state)
        h2 = layers.Dense(16, activation="relu")(h1)
        mu = layers.Dense(self._vh.action_size, activation="softplus")(h2)
        std = layers.Dense(self._vh.action_size, activation="sigmoid")(h2)
        outputs = [mu, std]
        return models.Model(inputs=state, outputs=outputs)

    def _build_value_net(self):
        return models.Sequential([
            layers.Dense(32, input_shape=(self._vh.state_size,), activation="relu"),
            layers.Dense(16, activation="relu"),
            layers.Dense(1, activation="linear")
        ])

    def get_action(self, state):
        state = state.reshape(1, self._vh.state_size)
        mu, std = self._policy_net.predict(state)
        action = np.random.normal(mu, std)
        prob = get_prob(mu, std, action)
        return action, prob

    def train(self, transitions):
        if len(transitions) >= self._vh.sample_size:
            self.train_timer.initialize()
            for update in range(int(self._vh.updates_n)):
                random.shuffle(transitions)
                for transition_batch in to_batch(transitions, self._vh.batch_size):
                    # split transitions
                    states, old_actions, rewards, next_states, dones, old_probs = split_transitions(transition_batch)
                    # train value net
                    values = train_value_net(self._value_net, self.optimizer(self._vh.lr_value_net), states, rewards)
                    # get advantages
                    advantages = get_gae(self._vh, rewards, (1 - dones), values)
                    # train policy net
                    train_policy_net(self._policy_net, self.optimizer(self._vh.lr_policy_net), self._vh.epsilon,
                                     states, old_actions, old_probs, advantages)
                    self._bot.step()
            self.train_timer.time()
            transitions.clear()

    def save_model(self):
        if not os.path.exists("./save_model"):
            os.mkdir("./save_model")
        self._policy_net.save("./save_model/policy_net.h5")
        self._value_net.save("./save_model/value_net.h5")

    def __call__(self):
        transitions = []
        for episode in range(int(self._vh.total_episodes)):
            self.episode_timer.initialize()
            state = self._env.reset()
            score = 0
            done = False
            probs = []
            timestep = 0
            while not done:
                self._bot.step()
                action, prob = self.get_action(state)
                next_state, reward, done, _ = self._env.step(action)
                score += reward
                probs.append(prob)
                transitions.append(Transition(state, action, reward, next_state, done, prob))
                state = next_state
                self.train(transitions)
                timestep += 1
            self.episode_timer.time()
            self._bot.add_status(
                {"episode": episode, "score": score[0], "avg_prob": np.mean(probs),
                 "cpu_percent": psutil.cpu_percent(), "timestep": timestep,
                 "train_time_avg": self.train_timer.mean_time, "episode_time_avg": self.episode_timer.time()})
            print(f"episode:{episode}")
            self.save_model()
