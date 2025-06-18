from torch import nn, torch
import torch.nn.functional as F
import os

class BirdBrain(nn.Module):
    def __init__(self):
        super(BirdBrain, self).__init__()
        
        # Layer sizes: 4 -> 10 -> 10 -> 2
        self.fc1 = nn.Linear(4, 10)   
        self.fc2 = nn.Linear(10, 10)   
        self.out = nn.Linear(10, 2)   

    def forward(self, x):
        x = F.relu(self.fc1(x))     
        x = F.relu(self.fc2(x))     
        x = self.out(x)       
        return x
    
    def save(self, path):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        torch.save(self.state_dict(), path)

    def load(self, path):
        self.load_state_dict(torch.load(path))
        self.eval()


class SnakeBrain(nn.Module):
    def __init__(self):
        super(SnakeBrain, self).__init__()
        # input: head_position (x,y), food position (x, y), distance from food (x,y), 
        # binary direction of food (left, right, down, up), danger of 4 possible moves (snake hits himself),
        # snake lenght, last direction
        # output: one of the possible directions 0:left, 1:up, 2:right, 3:down
        # Layer sizes: 7 -> 40 -> 40 -> 4
        self.fc1 = nn.Linear(16, 64)   
        self.fc2 = nn.Linear(64, 32)   
        self.fc3 = nn.Linear(32, 16)
        self.out = nn.Linear(16, 4)      

    def forward(self, x):
        x = F.relu(self.fc1(x))    
        x = F.relu(self.fc2(x))
        x = F.relu(self.fc3(x))     
        x = self.out(x)       
        return x
    
    def save(self, path):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        torch.save(self.state_dict(), path)

    def load(self, path):
        self.load_state_dict(torch.load(path))
        self.eval()