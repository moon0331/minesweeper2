"""Source: https://dksshddl.tistory.com/entry/%EA%B0%95%ED%99%94%ED%95%99%EC%8A%B5-tensorflow-2%EB%A1%9C-DQN"""

import random
from collections import deque

import tensorflow as tf
from tensorflow.keras.layers import Dense

import numpy as np
import matplotlib.pyplot as plt
import gym
from gym import spaces
# from IPython import display

# Hyperparameters
LEARNING_RATE = 0.0005
GAMMA         = 0.98
BUFFER_SIZE  = 50000
BATCH_SIZE    = 32
TARGET_UPDATE_ITER = 20


class ReplayBuffer:

    def __init__(self, buffer_size):
        self.buffer_size = buffer_size
        self.buffer = deque(maxlen=self.buffer_size)

    def sample(self, batch_size):
        size = batch_size if len(self.buffer) > batch_size else len(self.buffer)
        return random.sample(self.buffer, size)
    
    def clear(self):
        self.buffer.clear()

    def append(self, transition):
        self.buffer.append(transition)
    
    def __len__(self):
        return len(self.buffer)


class DQN(tf.keras.Model):

    def __init__(self, obs_dim, acs_dim):
        super(DQN, self).__init__()
        self.fc1 = Dense(128, activation='relu', kernel_initializer='he_uniform')
        self.fc2 = Dense(128, activation='relu', kernel_initializer='he_uniform')
        self.fc3 = Dense(acs_dim, activation='linear', kernel_initializer='he_uniform')
        self.build(input_shape=(None,) + obs_dim)
    
    def call(self, x):
        x = self.fc1(x)
        x = self.fc2(x)
        return self.fc3(x)


class TF2DQNAgent:

    def __init__(self, env, obs_dim, acs_dim, steps, gamma=0.99, epsilon=1.0, epsilon_decay=0.999, buffer_size=2000,
                batch_size=64, target_update_iter=100):
        self.env = env
        self.obs_dim = obs_dim
        self.acs_dim = acs_dim
        self.steps = steps
        self.gamma = gamma
        self.epsilon = epsilon
        self.epsilon_decay = epsilon_decay
        self.buffer_size = buffer_size
        self.batch_size = batch_size
        self.target_update_iter = target_update_iter

        self.replay_buffer = ReplayBuffer(self.buffer_size)

        self.q_net = DQN(self.obs_dim, self.acs_dim)
        self.q_target_net = DQN(self.obs_dim, self.acs_dim)

        self.q_net.compile(optimizer='adam', loss='mse')
        self.target_update()

        # self.loss_fn = tf.keras.losses.MeanSquaredError()
        self.loss_fn = tf.keras.losses.Huber()
        self.optimizer = tf.keras.optimizers.Adam()

    @tf.function
    def learn(self, obs, acs, next_obs, rewards, dones):
        # print(self.q_target_net(next_obs))
        # print(tf.reduce_max(self.q_target_net(next_obs), axis=1, keepdims=True))
        # print()

        q_target = rewards + (1 - dones) * self.gamma * tf.reduce_max(self.q_target_net(next_obs), axis=1, keepdims=True)

        with tf.GradientTape() as tape:
            q_pred = self.q_net(obs)
            acs_one_hot = tf.one_hot(tf.cast(tf.reshape(acs, [-1]), tf.int32), self.acs_dim)
            q_pred = tf.reduce_sum(q_pred * acs_one_hot, axis=1, keepdims=True)
            loss = self.loss_fn(q_target, q_pred)
        
        grads = tape.gradient(loss, self.q_net.trainable_weights)
        self.optimizer.apply_gradients(zip(grads, self.q_net.trainable_weights))
    
    def train(self):
        epochs = 0
        self.global_steps = 0
        rewards = []

        while self.global_steps < self.steps:
            ob = env.reset()
            reward = 0
            while True:
                ac = self.select_action(ob)
                next_ob, r, done, _ = env.step(ac)

                transition = (ob, ac, next_ob, r, done)
                self.replay_buffer.append(transition)

                reward += r
                ob = next_ob

                if done:
                    rewards.append(reward)
                    self.target_update()
                    # print("Epochs: %d / Score: %d" % (epochs + 1, reward))
                    print("n_episode: {}, score: {:.1f}, n_buffer: {}, eps: {:.1f}%".format(epochs, reward, len(self.replay_buffer), self.epsilon * 100))
                    break

                self.env.render()

                if self.global_steps > 1000:
                    transitions = self.replay_buffer.sample(batch_size=self.batch_size)
                    self.learn(*map(lambda x: np.vstack(x).astype('float32'), np.transpose(transitions)))
                
                self.global_steps += 1
        
            epochs += 1
        
        # plt.title('CartPole-v1')
        # plt.xlabel('epochs')
        # plt.ylabel('rewards')
        # plt.plot(rewards)
        # plt.show()
    
    def test(self):
        pass

    def target_update(self):
        self.q_target_net.set_weights(self.q_net.get_weights())
    
    def select_action(self, ob):
        # self.epsilon *= self.epsilon_decay
        # self.epsilon = max(0.01, self.epsilon)
        self.epsilon = max(0.01, 0.08 - 0.01*(self.global_steps / 200))
        if np.random.rand() <= self.epsilon:
            return np.random.randint(self.acs_dim)
        else:
            action = self.q_net(ob[np.newaxis])
            return np.argmax(action[0])


if __name__ == '__main__':
    tf.keras.backend.set_floatx('float32')
    env = gym.make('CartPole-v1')

    obs_dim = env.observation_space.shape
    acs_dim = None

    if isinstance(env.action_space, spaces.Box):
        acs_type = 'continuous'
        acs_dim = env.action_space.shape
    elif isinstance(env.action_space, spaces.Discrete):
        acs_type = 'discrete'
        acs_dim = env.action_space.n
    else:
        raise NotImplementedError('Not implemented')
    
    tf2_dqn_agent = TF2DQNAgent(env, obs_dim, acs_dim, 10000, gamma=GAMMA, buffer_size=BUFFER_SIZE, batch_size=BATCH_SIZE,
                        target_update_iter=TARGET_UPDATE_ITER)
    tf2_dqn_agent.train()