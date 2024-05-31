import cv2
import numpy as np
from collections import deque
import math

def clip(x: int | float) -> int:
    return max(0, min(255, int(x)))

def atan2(x: float, y: float) -> float:
    ret = math.atan2(x, y)
    
    if ret > 0:
        return ret
    
    else:
        return ret + 2 * math.pi
    
def direction(x, y):
    THRESH_R = 2 / (3 * math.sqrt(math.pi))
    dat_type = -1
    
    if math.sqrt(x ** 2 + y ** 2) < THRESH_R:
        dat_type = 0
        
    else:
        at = atan2(x, y)
        
        for i in range(2, 9):
            if (2 * i - 3) * (math.pi / 8) < at <= (2 * i - 1) * (math.pi / 8):
                dat_type = i

        if dat_type == -1:
            dat_type = 1
            
    return dat_type

N = 500
KF = 20

MOVEMENTS = [
    "No movement",
    "Right",
    "Upper right",
    "Up",
    "Upper left",
    "Left",
    "Lower left",
    "Down",
    "Lower right",
]


img = np.zeros((N, N), dtype=np.uint8)
mpos = deque([(0, 0) for _ in range(KF + 1)], maxlen=KF + 1)
cnt = 0

def onMouse(event, x, y, flags, param):
    global mpos, cnt

    mpos.append((x, y))
    
    x0, y0 = mpos[0]
    
    movement = direction(
        -(y - y0) / N,
        (x - x0) / N,
    )
    
    print(F"Call: {(cnt := cnt + 1) :07.0f}, Movement: {MOVEMENTS[movement]}")
    
    img = np.zeros((N, N), dtype=np.uint8)
    
    for i in range(KF + 1):
        cv2.circle(img, mpos[i], 10, (clip(255 * i / KF), clip(255 * i / KF), clip(255 * i / KF)), -1)
        
    cv2.imshow('asdf', img)

cv2.imshow('asdf', img)
cv2.setMouseCallback('asdf', onMouse)
cv2.waitKey()
cv2.destroyAllWindows()