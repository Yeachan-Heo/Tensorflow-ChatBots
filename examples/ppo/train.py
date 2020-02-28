import tensorflow as tf
from utils import *


# @tf.function
def train_value_net(model, optimizer, states, rewards):
    with tf.GradientTape() as tape:
        values = model(states)
        loss = tf.losses.mean_squared_error(values, rewards)
    grads = tape.gradient(loss, model.trainable_variables)
    optimizer.apply_gradients(zip(grads, model.trainable_variables))
    return values


# @tf.function
def train_policy_net(model, optimizer, epsilon, states, old_actions, old_probs, advantages):
    with tf.GradientTape() as tape:
        mu, std = model(states)
        new_probs = get_prob(mu, std, old_actions)
        ratio = old_probs / new_probs
        loss = -tf.clip_by_value(ratio, 1 - epsilon, 1 + epsilon) * tf.cast(advantages, tf.float32)
    grads = tape.gradient(loss, model.trainable_variables)
    optimizer.apply_gradients(zip(grads, model.trainable_variables))
