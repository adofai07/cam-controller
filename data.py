import math
import random
import tqdm
import pickle
import pandas as pd
import numpy as np
import torch
from torch import nn
from torch.utils.data import DataLoader, TensorDataset

def atan2(x: float, y: float) -> float:
    ret = math.atan2(x, y)
    
    if ret > 0:
        return ret
    
    else:
        return ret + 2 * math.pi
    
def one_hot(x: int) -> list[int]:
    ret = [0 for _ in range(9)]
    
    ret[x] = 1
    
    return ret

ATAN2 = atan2
SQRT = math.sqrt
TAN = math.tan
PI = math.pi

L = []
positions = []
classes = []
N = 100_000
cnts = [0 for _ in range(9)]
THRESH_R = 2 / (3 * SQRT(PI))

# 0 | No movement
# 1 | Right
# 2 | Upper right
# 3 | Up
# 4 | Upper left
# 5 | Left
# 6 | Lower left
# 7 | Down
# 8 | Lower right

pbars = [
    tqdm.tqdm(total=N, position=i, ascii=True, leave=False)
    for i in range(9)
]

while sum((cnts[i] - N) for i in range(9)):
    x, y = random.uniform(-1, 1), random.uniform(-1, 1)
    pts = [[0, 0]]
    
    for i in range(1, 9):
        pts.append(
            [
                x * (i / 9),
                y * (i / 9)
            ]
        )
        
    pts.append([x, y])
    
    dat_type = -1
    
    if SQRT(x ** 2 + y ** 2) < THRESH_R:
        dat_type = 0
        
    else:
        at = ATAN2(x, y)
        
        for i in range(2, 9):
            if (2 * i - 3) * (PI / 8) < at <= (2 * i - 1) * (PI / 8):
                dat_type = i

        if dat_type == -1:
            dat_type = 1
            
    
    if cnts[dat_type] < N:
        cnts[dat_type] += 1
        L.append([*pts, dat_type])
        
        pbars[dat_type].update(1)
    
for i in range(9):
    pbars[i].close()

print()
print("Shuffling...")
random.shuffle(L)

for i in tqdm.trange(N * 9):
    positions.append(L[i][:-1])
    classes.append(one_hot(L[i][-1]))
    
train_data = TensorDataset(
    torch.Tensor(positions),
    torch.Tensor(classes)
)

with open(F"tensor_dataset.asdf", "wb+") as f:
    pickle.dump(train_data, f)