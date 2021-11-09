import cv2
import numpy as np
import pandas as pd
import time
import math

update_int = 0.1
d = (600,800) #height, width
timeout = 100

def merge_frames(back, front):
    frame = cv2.addWeighted(back,0.4,front,0.1,0)
    return frame;

if __name__ == "__main__":

    frame_back = np.zeros((d[0],d[1],4), np.uint8)
    frame_front = np.zeros((d[0],d[1],4), np.uint8)
    frame_front[:,:,3] = np.ones((d[0],d[1]))*255;
    n = 0.0;
    while True:

        v1 = math.sin(n/10)
        v2 = math.cos(n/30)
        frame_back[:,0:d[1]//2] = (v1*255,0,0,0)      # (B, G, R)
        frame_back[:,d[1]//2:d[1]] = (0,v2*255,0,0)
        frame = merge_frames(frame_back, frame_front)
        cv2.imshow( "output", frame)

        n+=1
        time.sleep(0.01)
        if cv2.waitKey(1) & 0xFF == ord( 'x' ):
            break
        if n > timeout:
            break

    input.release()
    cv2.destroyAllWindows()



'''
import cv2
2
3 cap = cv2.VideoCapture('vtest.avi')
4
5 while(cap.isOpened()):
6 ret, frame = cap.read()
7 gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
8 cv2.imshow('frame',gray)
9
10 if cv2.waitKey(1) & 0xFF == ord('q'):
11 break
12 cap.release()
13 cv2.destroyAllWindows()
'''
