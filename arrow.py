import math
import cv2
import numpy as np
from collections import deque

def increase_brightness(img, value=30):
    if value > 0:
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        h, s, v = cv2.split(hsv)

        lim = 255 - value
        v[v > lim] = 255
        v[v <= lim] += value

        final_hsv = cv2.merge((h, s, v))
        img = cv2.cvtColor(final_hsv, cv2.COLOR_HSV2BGR)
        
    if value < 0:
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        h, s, v = cv2.split(hsv)

        lim = -value
        v[v < lim] = 0
        v[v >= lim] -= -value

        final_hsv = cv2.merge((h, s, v))
        img = cv2.cvtColor(final_hsv, cv2.COLOR_HSV2BGR)
        
    return img

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

N = 400
BR = 130

ONES = np.ones((N, N), dtype=np.int32)

XGR = np.array(
    [
        [i for i in range(N)]
        for j in range(N)
    ],
    dtype=np.int32
)

YGR = np.array(
    [
        [j for i in range(N)]
        for j in range(N)
    ],
    dtype=np.int32
)

cap = cv2.VideoCapture(0)
frames = deque(maxlen=4)
fcnt = 0
pts = deque(maxlen=15)

for _ in range(100):
    pts.append(None)

if cap.isOpened():
    while True:
        ret, img = cap.read()

        if ret:
            fcnt += 1
            
            img = img[:, ::-1, :]
            brightness = round(np.mean(img))
            
            img = img[
                ((img.shape[0] - N) // 2):((img.shape[0] + N) // 2),
                ((img.shape[1] - N) // 2):((img.shape[1] + N) // 2),
            ]
            
            # cv2.imshow('qwer', img)
            arrow = img.copy()
            
            img = increase_brightness(img, BR - brightness)
            
            # print(F"Frame: {fcnt :>8}, Brightness: {brightness :>3} -> {(brightness := round(np.mean(img))) :>3}")
            frames.append(img)
            
            if fcnt <= 20:
                print(F"Collecting frames: {fcnt} / 10")
                
            else:
                prev = frames[0].copy()
                curr = frames[-1].copy()
                
                img1 = cv2.blur(prev, (5, 5))
                img2 = cv2.blur(curr, (5, 5))
                
                diff = cv2.absdiff(img1, img2)
                
                _, mask = cv2.threshold(cv2.cvtColor(diff, 6), 10, 255, cv2.THRESH_BINARY)
                curr[mask != 255] = [0, 0, 0]
                
                # cv2.imshow('asdf', curr)
                
                mask = cv2.inRange(
                    curr.copy(),
                    np.array([0, 85, 0]),
                    np.array([80, 200, 80])
                ).astype(np.int32)
                                
                curr = frames[-1].copy()
                
                CNT = np.sum(mask * ONES) // 255
                
                if CNT >= 50:
                    CMX = round((np.sum(mask * XGR) // 255) / CNT)
                    CMY = round((np.sum(mask * YGR) // 255) / CNT)
                    
                    pts.append((CMX, CMY))
                    
                    # print(F"({CMX :>4}, {CMY :>4}), {CNT = }")
                    # print(mask)
                    
                    cv2.circle(curr, (CMX, CMY), 10, (0, 255, 0), -1)
                    
                else:
                    pts.append(None)
                    
                if pts.count(None) < 4:
                    cnt = len(pts) - pts.count(None) - 1
                    
                    st, ed = 0, -1
                    
                    while pts[st] is None:
                        st += 1
                        cnt -= 1
                    
                    while pts[ed] is None:
                        ed -= 1
                        cnt -= 1
                    
                    cv2.circle(arrow, (N // 2, N // 2), N // 2 - 10, (0, 0, 255), 10)
                    
                    d = direction(
                        ((pts[ed][1] - pts[st][1]) / (N * cnt)) * 17,
                        ((pts[ed][0] - pts[st][0]) / (N * cnt)) * 17,
                    )
                    
                    print(F"Direction: {d}")
                    
                    if d == 0:
                        cv2.circle(arrow, (round(N * 0.5), round(N * 0.5)), 30, (0, 0, 255), -1)
                        
                    else:
                        cv2.circle(arrow, (round(N * 0.5 + (N * 0.2) * math.cos((math.pi / 4) * (d - 1))), round(N * 0.5 + (N * 0.2) * math.sin((math.pi / 4) * (d - 1)))), 30, (0, 0, 255), -1)
                        
                
                # curr[mask == 0] = [0, 0, 0]
                # curr[mask != 0] = [255, 255, 255]
                
                cv2.imshow('asdf', curr)
                cv2.imshow('zxcv', mask.astype(np.uint8))
                cv2.imshow('arrow', arrow)
            
            # cv2.imshow('asdf', img)

            if cv2.waitKey(1) & 0xFF == 0x1B:
                break

        else:
            print('No frame')
            break
        
else:
    print("asdfasdf")
    
cap.release()
cv2.destroyAllWindows()