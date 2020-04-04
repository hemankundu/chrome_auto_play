import time
import numpy as np
from mss import mss
import pyautogui as ag
import cv2

#algo
# 1. Capture a small rectangular portion of screen (watch window)
# 2. Calculate mean for left and right halves of the captured rectangle
# 3. Depending on difference betwwen the mean values, perform a key press

def reset():
    print('reset..')
    return (0.09, 0, 565)


sct = mss()
#these are the parametrs to play with
jump_delay = 0.09 #delay between detecting an obstacle and reacting (jump) to it
jump_cnt = 0 # number of times jumped. Helps adjusting other parametrs as game speed increases
left = 565 # distance between the character and the watch window
while 1:
    # uncomment follwing two lines to set watch window at mouse pionet location
    # mouse_position = ag.position()
    # mon = {'top': mouse_position.y, 'left': mouse_position.x, 'width': 40, 'height': 100}  

    # Using fixed position for watch window  
    mon = {'top': 564, 'left': left, 'width': 40, 'height': 100} 
    img = sct.grab(mon)
    img_arr = np.array(img)
    left_mean = np.mean(img_arr[:, :20, :])
    right_mean = np.mean(img_arr[:, 20:, :])

    # top_mean = np.mean(img_arr[50:, :, :])
    # bottom_mean = np.mean(img_arr[:50, :, :])
    
    left_right = int(abs(left_mean - right_mean))
    # top_bottom = int(abs(top_mean - bottom_mean))
    
    if left_right > 5:
        time.sleep(jump_delay)
        jump_delay -= (jump_delay * 0.005)
        ag.press('space')
        print('space:', end=' ')
        # print(jump_cnt, left_right, mouse_position, left ,jump_delay)
        print(jump_cnt, left_right, left ,jump_delay)
        jump_cnt += 1
        if jump_cnt%40 == 0:
            left += 15
            jump_delay -= 0.01
        cv2.imshow('Capture', img_arr)
        # time.sleep(.05)
    if cv2.waitKey(10) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        break
    elif cv2.waitKey(10) & 0xFF == ord('r'):
        jump_delay, jump_cnt, left = reset()
