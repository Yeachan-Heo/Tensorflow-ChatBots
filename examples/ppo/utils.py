from numba import jit
import numpy as np
import tensorflow as tf
import random


class Transition(object):
    def __init__(self, state, action, reward, next_state, done, prob):
        self.state, self.action, self.reward, self.next_state, self.done, self.prob \
            = state, action, reward, next_state, done, prob


def split_transitions(transitions: [Transition]):
    states = np.array(list(map(lambda x: x.state, transitions)))
    actions = np.array(list(map(lambda x: x.action, transitions)))
    rewards = np.array(list(map(lambda x: x.reward, transitions)))
    next_states = np.array(list(map(lambda x: x.next_state, transitions)))
    dones = np.array(list(map(lambda x: x.done, transitions))).astype(np.bool)
    probs = np.array(list(map(lambda x: x.prob, transitions)))
    return states, actions, rewards, next_states, dones, probs


def get_prob(mu, std, action):
    var = std ** 2
    log_prob = -0.5 * (action - mu) ** 2 / var - 0.5 * tf.math.log(var * 2 * np.pi)
    prob = tf.exp(log_prob)
    return prob


@jit
def to_batch(transitions, batch_size):
    batch_indexes = list(range(0, len(transitions), batch_size))
    batch_indexes = batch_indexes if batch_indexes[-1] == len(transitions) else batch_indexes + [100]
    batch_transitions = list(map(lambda x: transitions[x[0]:x[1]], zip(batch_indexes[:-1], batch_indexes[1:])))
    return batch_transitions
