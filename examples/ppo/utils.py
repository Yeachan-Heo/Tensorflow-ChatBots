import numpy as np
import tensorflow as tf


class Transition(object):
    def __init__(self, state, action, reward, next_state, done, log_prob):
        self.state, self.action, self.reward, self.next_state, self.done, self.log_prob \
            = state, action, reward, next_state, done, log_prob


def split_transitions(transitions: [Transition]):
    states = np.array(list(map(lambda x: x.state.squeeze(), transitions)))
    actions = np.array(list(map(lambda x: x.action, transitions)))
    rewards = np.array(list(map(lambda x: x.reward, transitions)))
    next_states = np.array(list(map(lambda x: x.next_state.squeeze(), transitions)))
    dones = np.array(list(map(lambda x: x.done, transitions))).astype(np.int32)
    log_probs = np.array(list(map(lambda x: x.log_prob, transitions))).squeeze()
    return states, actions, rewards, next_states, dones, log_probs


def get_log_prob(mu, std, action):
    var = std ** 2
    log_prob = -0.5 * (action - mu) ** 2 / var - 0.5 * tf.math.log(var * 2 * np.pi)
    return log_prob


def to_batch(transitions, batch_size):
    batch_indexes = list(range(0, len(transitions), batch_size))
    batch_indexes = batch_indexes if batch_indexes[-1] == len(transitions) else batch_indexes + [len(transitions)]
    batch_transitions = list(map(lambda x: transitions[x[0]:x[1]], zip(batch_indexes[:-1], batch_indexes[1:])))
    return batch_transitions


def get_gae(vh, rewards, masks, values):
    returns = np.zeros_like(rewards)
    advants = np.zeros_like(rewards)

    running_returns = 0
    previous_value = 0
    running_advants = 0

    for t in reversed(range(0, len(rewards))):
        running_returns = rewards[t] + vh.gamma * running_returns * masks[t]
        running_tderror = rewards[t] + vh.gamma * previous_value * masks[t] - \
                          values[t]
        running_advants = running_tderror + vh.gamma * vh.lamda * \
                          running_advants * masks[t]

        returns[t] = running_returns
        previous_value = values[t]
        advants[t] = running_advants

    advants = (advants - advants.mean()) / advants.std()
    return returns, advants
