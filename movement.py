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
            
            cv2.imshow('qwer', img)
            
            img = increase_brightness(img, BR - brightness)
            
            print(F"Frame: {fcnt :>8}, Brightness: {brightness :>3} -> {(brightness := round(np.mean(img))) :>3}")
            frames.append(img)
            
            if fcnt <= 10:
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
                    
                    # print(F"({CMX :>4}, {CMY :>4}), {CNT = }")
                    # print(mask)
                    
                    cv2.circle(curr, (CMX, CMY), 10, (0, 255, 0), -1)
                
                # curr[mask == 0] = [0, 0, 0]
                # curr[mask != 0] = [255, 255, 255]
                
                cv2.imshow('asdf', curr)
                cv2.imshow('zxcv', mask.astype(np.uint8))
            
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