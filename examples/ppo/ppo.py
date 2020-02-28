from tensorflow_chatbots.variableholder.variableholder import VariableHolder
from tensorflow_chatbots.ttb.callback import TelegramBotCallback
from tensorflow.keras import *
from decorators import *
from utils import *
import tensorflow as tf
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
        if self._vh.is_continous:
            mu = layers.Dense(self._vh.action_size, activation="softplus")(h2)
            std = layers.Dense(self._vh.action_size, activation="sigmoid")(h2)
            outputs = [mu, std]
        else:
            outputs = layers.Dense(self._vh.action_size, activation="softmax")(h2)
        return models.Model(inputs=state, outputs=outputs)

    def _build_value_net(self):
        return models.Sequential([
            layers.Dense(32, input_shape=(self._vh.state_size,), activation="relu"),
            layers.Dense(16, activation="relu"),
            layers.Dense(1, activation="linear")
        ])

    @get_action_decorator
    def _get_action_continuous(self, policy_net_prediction):
        mu, std = policy_net_prediction
        action = np.random.normal(mu.numpy(), std.numpy())
        log_prob = get_log_prob(mu, std, action)
        return action, log_prob

    @get_action_decorator
    def _get_action_discrete(self, policy_net_prediction):
        prob = tf.math.log(policy_net_prediction)
        action = np.random.choice(np.arange(0, self._vh.action_size), p=prob)
        return action, tf.math.log(prob[action])

    @train_policy_net_decorator
    def _train_policy_net_continuous(self, prediction, actions):
        mu, std = prediction
        new_log_probs = get_log_prob(mu, std, actions)
        return new_log_probs

    @train_policy_net_decorator
    def _train_policy_net_discrete(self, prediction, actions):
        return tf.log(tf.reduce_sum(prediction*tf.one_hot(actions, depth=self._vh.action_size)))

    def _train_value_net(self, transitions):
        states, old_actions, rewards, next_states, dones, old_log_probs = split_transitions(transitions)
        with tf.GradientTape() as tape:
            values = self._value_net(states)
            returns, advantages = get_gae(self._vh, rewards, (1 - dones), values)
            loss = tf.losses.mean_squared_error(values, returns)
        grads = tape.gradient(loss, self._value_net.trainable_variables)
        self.optimizer(self._vh.lr_value_net).apply_gradients(zip(grads, self._policy_net.trainable_variables))
        return advantages

    def train(self, transitions):
        if len(transitions) >= self._vh.sample_size:
            for update in range(int(self._vh.updates_n)):
                random.shuffle(transitions)
                for transition_batch in to_batch(transitions, self._vh.batch_size):
                    advantages = self._train_value_net(transition_batch)
                    self.train_policy_net(transition_batch, advantages)
                    self._bot.step()
            transitions.clear()

    def save_model(self):
        if not os.path.exists("./save_model"):
            os.mkdir("./save_model")
        self._policy_net.save("./save_model/policy_net.h5")
        self._value_net.save("./save_model/value_net.h5")

    def __call__(self):
        transitions = []
        for episode in range(int(self._vh.total_episodes)):
            state = self._env.reset()
            score = 0
            done = False
            log_probs = []
            timestep = 0
            while not done:
                self._bot.step()
                action, log_prob = self.get_action(state)
                next_state, reward, done, _ = self._env.step(action)
                score += reward
                log_probs.append(log_prob)
                transitions.append(Transition(state, action, reward, next_state, done, log_prob))
                state = next_state
                self.train(transitions)
            self._bot.add_status(
                {"episode": episode, "score": score, "avg_log_prob": np.mean(log_probs)[0],
                 "cpu_percent": psutil.cpu_percent(), "timestep": timestep})
            print(f"episode:{episode}")
            self.save_model()
