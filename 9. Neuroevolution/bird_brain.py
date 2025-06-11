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