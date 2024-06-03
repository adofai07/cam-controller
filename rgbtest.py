import cv2
import numpy as np
from collections import deque
import colorsys

def rgb_to_hsv(r, g, b):
    c = colorsys.rgb_to_hsv(r, g, b)

N = 400

cap = cv2.VideoCapture(0)
frames = deque(maxlen=3)
fcnt = 0

if cap.isOpened():
    while True:
        ret, img = cap.read()

        if ret:
            fcnt += 1
            img = img[
                ((img.shape[0] - N) // 2):((img.shape[0] + N) // 2),
                ((img.shape[1] - N) // 2):((img.shape[1] + N) // 2),
            ]
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
                
                if curr[200, 200].any():
                    print(curr[200, 200])
                
                diff_rgb = np.zeros((N, N * 3, 3), dtype=np.uint8)
                
                diff_rgb[:, N * 0:N * 1, 2] = curr[:, :, 2]
                diff_rgb[:, N * 1:N * 2, 1] = curr[:, :, 1]
                diff_rgb[:, N * 2:N * 3, 0] = curr[:, :, 0]
                
                # cv2.imshow('asdf', curr)
                cv2.imshow('asdf', diff_rgb)
            
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