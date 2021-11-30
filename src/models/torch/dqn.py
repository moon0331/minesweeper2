import random
import torch.nn as nn
import torch.nn.functional as F


class QNet(nn.Module):

    def __init__(self, action_size):
        super(QNet, self).__init__()
        self.fc1 = nn.Linear(4, 128)
        self.fc2 = nn.Linear(128, 128)
        self.fc3 = nn.Linear(128, action_size)
        self.action_size = action_size

    def forward(self, x):
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = self.fc3(x)
        return x
    
    def sample_action(self, obs, epsilon):
        out = self.forward(obs)
        prob = random.random()
        if prob < epsilon:
            return random.randint(0, self.action_size - 1)
        else:
            return out.argmax().item()