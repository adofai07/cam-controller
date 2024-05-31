import cv2
import numpy as np

win_name = "video"
frames = []  

cap = cv2.VideoCapture(0) 

if cap.isOpened():    
    while True:
        ret, frame = cap.read()
        if ret:            
            
            key = cv2.waitKey(1) & 0xFF
            if key == 27: break
                        
            
            frames.append(frame)
            if(len(frames) > 3):
                frames = frames[1:]
                gray_frames = []
                for i in range(3): gray_frames.append(cv2.cvtColor(frames[i], cv2.COLOR_BGR2GRAY))
            
            
            
                diff1 = cv2.absdiff(gray_frames[0], gray_frames[1])
                diff2 = cv2.absdiff(gray_frames[1], gray_frames[2])

                move = cv2.bitwise_and(diff1, diff2)
            
            
                _, mask = cv2.threshold(move, 10, 255, cv2.THRESH_BINARY)
                frame[mask==255] = [0,255,0]
                frame = cv2.blur(frame, (3,3))

                cv2.imshow(win_name, frame)
            
        else:
            print('no frame!!!')
            break
            
cap.release()
cv2.destroyAllWindows()     