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
        # input: head_position_x, head_position_y, food position_x, food_position_y, 
        # distance from food x, distance from food y, normalized distance, curr_direction
        # output: one of the possible directions 0:left, 1:up, 2:right, 3:down
        # Layer sizes: 7 -> 40 -> 40 -> 4
        self.fc1 = nn.Linear(8, 40)   
        self.fc2 = nn.Linear(40, 40)   
        self.out = nn.Linear(40, 4)   

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