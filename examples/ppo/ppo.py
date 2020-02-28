from tensorflow_chatbots.variableholder.variableholder import VariableHolder
from tensorflow_chatbots.ttb.callback import TelegramBotCallback
from tensorflow.keras import *
from .decorators import *
from .utils import *
import tensorflow as tf
import numpy as np
import gym
import os


class PPO(object):
    def __init__(self, **kwargs):
        self._env = None
        self._vh = VariableHolder(**kwargs)
        self._policy_net = self._build_policy_net()
        self._value_net = self._build_value_net()
        self._bot = TelegramBotCallback(token=self._vh.token)
        self.optimizer = optimizers.Adam

        self.train_policy_net = self._train_policy_net_continuous \
            if self._vh.is_continous \
            else self._train_policy_net_discrete
        self.get_action = self._get_action_continuous \
            if self._vh.is_continous \
            else self._get_action_discrete

    def set_env(self, env: gym.Env or str):
        self._env = env \
            if isinstance(env, gym.Env) \
            else gym.make(env)

    def _build_policy_net(self):
        state = layers.Input(shape=(self._vh.state_size,))
        h1 = layers.Dense(32, activation="relu")(state)
        h2 = layers.Dense(16, activation="relu")(h1)
        if self._vh.is_contionus:
            mu = layers.Dense(self._vh.action_size, activation="linear")(h2)
            std = layers.Dense(self._vh.action_size, activation="linear")(h2)
            outputs = [mu, std]
        else:
            outputs = layers.Dense(self._vh.action_size, activation="softmax")(h2)
        return models.Model(inputs=state, outputs=outputs)

    def _build_value_net(self):
        return models.Sequential([
            layers.Dense(32, input_shape=(self.vh.state_size,), activation="relu"),
            layers.Dense(16, activation="relu"),
            layers.Dense(1, activation="linear")
        ])

    @get_action_decorator
    def _get_action_continuous(self, policy_net_prediction):
        mu, std = policy_net_prediction
        action = np.random.normal(mu.numpy(), std.numpy())
        prob = get_prob(mu, std, action)
        return action, prob

    @get_action_decorator
    def _get_action_discrete(self, policy_net_prediction):
        prob = policy_net_prediction
        action = np.random.choice(np.arange(0, self._vh.action_size), p=prob)
        return action, prob[action]

    @train_policy_net_decorator
    def _train_policy_net_continuous(self, prediction):
        mu, std = prediction
        new_actions = tf.random.normal(mean=mu, stddev=std)
        new_probs = get_prob(mu, std, new_actions)
        return new_probs

    @train_policy_net_decorator
    def _train_policy_net_discrete(self, prediction):
        return prediction

    def _train_value_net(self, transitions):
        states, old_actions, rewards, next_states, dones, old_log_probs = split_transitions(transitions)
        with tf.GradientTape() as tape:
            values = self._value_net(states)
            loss = tf.losses.mean_squared_error(values, rewards)
        grads = tape.gradient(loss, self._value_net.trainable_variables)
        self.optimizer(self._vh.lr_value_net).apply_gradients(zip(grads, self._policy_net.trainable_variables))
        return values

    def train(self, transitions):
        if len(transitions) >= self._vh.sample_size:
            for update in range(int(self._vh.updates_n)):
                for transition_batch in to_batch(random.shuffle(transitions), self._vh.batch_size):
                    values = self._train_value_net(transition_batch)
                    self.train_policy_net(transition_batch, values)
        transitions.clear()

    def save_model(self):
        if not os.path.exists("./save_model"):
            os.mkdir("./save_model")
        self._policy_net.save("./save_model/policy_net.h5")
        self._value_net.save("./save_model/value_net.h5")

    def main_loop(self):
        transitions = []
        for episode in range(int(self._vh.total_episodes)):
            state = self._env.reset()
            score = 0
            done = False
            while not done:
                action, prob = self.get_action(state)
                next_state, reward, done, _ = self._env.step(action)
                score += reward
                transitions.append(Transition(state, action, reward, next_state, done, prob))
                self.train(transitions)
