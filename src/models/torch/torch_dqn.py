import random
import numpy as np
from collections import deque

import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

DISCOUNT_RATE = 0.98
LEARNING_RATE = 0.0005
REPLAY_MEMORY = 50000
LEARNING_STARTS = 2000
TARGET_UPDATE_ITER = 20
EPSILON_START = 0.08
PATH = './q.pt'
BATCH_SIZE = 32


class ReplayMemory:
    def __init__(self):
        self.memory = deque(maxlen=REPLAY_MEMORY)
    
    def put(self, transition):
        self.memory.append(transition)
    
    def sample(self, n):
        mini_batch = random.sample(self.memory, n)
        states = []
        actions = []
        rewards = []
        next_states = []
        done_masks = []

        for transition in mini_batch:
            state, action, reward, next_state, done_mask = transition
            states.append(state)
            actions.append([action])
            rewards.append([reward])
            next_states.append(next_state)
            done_masks.append([done_mask])

        # Torch 성능 이슈로 인해 np.ndarray로 변환
        states = np.array(states)
        actions = np.array(actions)
        rewards = np.array(rewards)
        next_states = np.array(next_states)
        done_masks = np.array(done_masks)

        return torch.tensor(states, device=device, dtype=torch.float), torch.tensor(actions, device=device), \
                torch.tensor(rewards, device=device), torch.tensor(next_states, device=device, dtype=torch.float), \
                torch.tensor(done_masks, device=device)
    
    def size(self):
        return len(self.memory)


class TorchDQNAgent:
    def __init__(self, args):        
        print("=" * 100)
        print("Started Minesweeper2 DQN algorithm")
        print("=" * 100)

        # self.double = args['double']
        # self.multistep = args['multistep']
        # self.n_steps = args['n_steps']

        # self.trained_model = args['trained_model']
        # if self.trained_model:
        #     mode = 'Test trained model'
        # else:
        #     mode = 'Training model'
        
        # print("=" * 100)
        # print("Double : {}    Multistep : {}/{}steps    Train : {}    Test : {}    Mode : {}".format(
        #         self.double, self.multistep, self.n_steps, args['numTraining'], args['numTesting'], mode))
        # print("=" * 100)

        if self.trained_model:
            self.epsilon = 0
        else:
            self.epsilon = EPSILON_START

        self.win_counter = 0
        self.steps_taken = 0
        self.steps_per_epi = 0
        self.episode_number = 0
        self.episode_rewards = []  
        
        self.epsilon = EPSILON_START  # epsilon 초기값

        # Replay memory와 Q network 초기화
        self.input_size = 11  # 현재는 input size를 미리 주지만 input_size를 탐지하는 방법은 없나 고민중
        self.q = DQN(self.input_size).to(device)
        self.q_target = DQN(self.input_size).to(device)
        self.q_target.load_state_dict(self.q.state_dict())
        self.replay_memory = ReplayMemory()
        self.optimizer = optim.Adam(self.q.parameters(), lr=LEARNING_RATE)
    
    def predict(self, state): 
        state = self.preprocess(state)
        state = torch.from_numpy(state).float()

        # e-Greedy
        q_out = self.q(state)
        act_prob = random.random()
        if act_prob < self.epsilon:
            act = random.randint(0, 3)
        else:
            act = q_out.argmax().item()
        
        self.action = act
        return act
    
    def update_epsilon(self):
        self.epsilon = max(0.01, 0.08 - 0.01 * (self.episode_number / 200)) 
                 
    def step(self, next_state, reward, done):
        if self.action is None:
            self.state = self.preprocess(next_state)
        
        else:
            self.next_state = self.preprocess(next_state)
            
            # Transition을 replay memory에 보관
            done_mask = 0.0 if done else 1.0
            self.replay_memory.put((self.state, self.action, reward, self.next_state, done_mask))
            
            self.state = self.next_state
        
        self.episode_reward += reward
        self.steps_taken += 1
        self.steps_per_epi += 1

        if self.trained_model == False:
            self.q.train()
            if self.replay_memory.size() > LEARNING_STARTS:
                self.train()
            self.update_epsilon()
            if self.steps_taken % TARGET_UPDATE_ITER == 0:
                # Target network 업데이트
                self.q_target.load_state_dict(self.q.state_dict())
            
            torch.save(self.q.state_dict(), PATH)
        else:
            # Test mode
            self.q_target = DQN(self.input_size).to(device)
            self.q_target.load_state_dict(torch.load(PATH))
            self.q_target.eval()
		
    def train(self):
        # Replay memory로부터 mini-batch를 받아 policy를 업데이트
        for _ in range(10):
            state, action, reward, next_state, done_mask = self.replay_memory.sample(BATCH_SIZE)
            
            q_out = self.q(state)
            q_a = q_out.gather(1, action)
            max_q_prime = self.q_target(next_state).max(1)[0].unsqueeze(1)
            target = reward + DISCOUNT_RATE * max_q_prime * done_mask
            loss = F.smooth_l1_loss(q_a, target)

            self.optimizer.zero_grad()
            loss.backward()
            self.optimizer.step()

    def reset(self):
        self.last_score = 0
        self.current_score = 0
        self.episode_reward = 0

        self.episode_number += 1
        self.steps_per_epi = 0
    
    def final(self, state):
        # Epsidoe 종료 시 호출되는 함수
        done = True
        reward = self.getScore(state)
        if reward >= 0: # not eaten by ghost when the game ends
            self.win_counter +=1

        self.step(state, reward, done)
        self.episode_rewards.append(self.episode_reward)
        win_rate = float(self.win_counter) / 500.0

        avg_reward = np.mean(np.array(self.episode_rewards))
		# 에피소드 정보 출력
        if self.episode_number%500 == 0:
            print("Episode no = {:>5}; Win rate {:>5}/500 ({:.2f}); average reward = {:.2f}; epsilon = {:.2f}".format(self.episode_number,
                                                                    self.win_counter, win_rate, avg_reward, self.epsilon))
            self.win_counter = 0
            self.episode_rewards= []

    def preprocess(self, state):
        res = []
        # pacman_pos = state.getPacmanPosition()
        # ghost_pos = state.getGhostPosition(1)  # Max: 1
        # food_num = state.getNumFood()
       
        # if len(state.getCapsules()) == 1:
        #     capsule_pos = state.getCapsules()[0]
        # else:
        #     capsule_pos = (-1, -1)

        # food = state.getFood()
        # food_pos = []

        # # Get food position from food grid
        # for i in range(7):
        #     for j in range(7):
        #         if food[i][j]:
        #             food_pos.append([i, j])
        
        # # Feature vector
        # res = [pacman_pos[0], pacman_pos[1], ghost_pos[0], ghost_pos[1], food_num,
        #         capsule_pos[0], capsule_pos[1]]

        # # Concatenate food position to feature vector
        # if food_num == 2:
        #     res.extend([food_pos[0][0], food_pos[0][1], food_pos[1][0], food_pos[1][1]])
        # elif food_num == 1:
        #     res.extend([food_pos[0][0], food_pos[0][1], -1, -1])
        # else:
        #     res.extend([-1, -1, -1, -1])

        return np.array(res)


class DQN(nn.Module):
    def __init__(self, D_in):
        super(DQN, self).__init__()
        self.fc1 = nn.Linear(D_in, 128)
        self.fc2 = nn.Linear(128, 128)
        self.fc3 = nn.Linear(128, 4)
    
    def forward(self, x):
        x = x.to(device)
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = self.fc3(x)
        return x