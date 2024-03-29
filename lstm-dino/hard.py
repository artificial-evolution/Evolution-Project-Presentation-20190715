import numpy as np
from PIL import ImageGrab
import cv2
import cv2 as cv
import keyboard
import time
start = time.time()

template1 = cv.imread('images/cactus1.png', 0)
template2 = cv.imread('images/cactus2.png', 0)
template3 = cv.imread('images/bird1.png', 0)
template4 = cv.imread('images/bird2.png', 0)
w1, h1 = template1.shape[::-1]
w2, h2 = template2.shape[::-1]
w3, h3 = template3.shape[::-1]
w4, h4 = template4.shape[::-1]
 
def process_img(original_image):
    img_gray = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)
    return img_gray

f = open("dino.csv", 'w')

speed1 = 170
speed1 = 190
while(True):
    if keyboard.is_pressed('left'):
        start = time.time()
    data = [0, 0, 0, 0, 0, 0]
    screen =  np.array(ImageGrab.grab(bbox=(1135, 306, 1755, 426)))
    img_gray = process_img(screen)
    res1 = cv.matchTemplate(img_gray, template1, cv.TM_CCOEFF_NORMED)
    res2 = cv.matchTemplate(img_gray, template2, cv.TM_CCOEFF_NORMED)
    res3 = cv.matchTemplate(img_gray, template3, cv.TM_CCOEFF_NORMED)
    res4 = cv.matchTemplate(img_gray, template4, cv.TM_CCOEFF_NORMED)
    threshold = 0.8
    loc1 = np.where(res1 >= threshold)
    loc2 = np.where(res2 >= threshold)
    loc3 = np.where(res3 >= threshold)
    loc4 = np.where(res4 >= threshold)

    for pt in zip(*loc1[::-1]):
        cv.rectangle(img_gray, pt, (pt[0] + w1, pt[1] + h1), (0, 0, 255), 2)
        data[1] = pt[0]
        break
 
    for pt in zip(*loc2[::-1]):
        cv.rectangle(img_gray, pt, (pt[0] + w2, pt[1] + h2), (0, 0, 255), 2)
        data[2] = pt[0]
        break
 
    for pt in zip(*loc3[::-1]):
        cv.rectangle(img_gray, pt, (pt[0] + w3, pt[1] + h3), (0, 0, 255), 2)
        data[3] = pt[0]
        data[4] = pt[1]
        break
 
    for pt in zip(*loc4[::-1]):
        cv.rectangle(img_gray, pt, (pt[0] + w4, pt[1] + h4), (0, 0, 255), 2)
        data[3] = pt[0]
        data[4] = pt[1]
        break

    # 선인장 점프 로직
    if((data[1]<=speed1 and data[1]!=0) or (data[2]<=speed1 and data[2]!=0)):
        keyboard.press('space')
        data[5] = 1
    # 새 점프 로직 
    if(44<=data[4]<=55)or(76<=data[4]<=84):
        if(data[3]<=speed2 and data[3]!=0):
            keyboard.press('space')
            data[5] = 1

    speed1 = 170 + (time.time() - start)
    speed2 = 190 + (time.time() - start)
    print(speed1,speed2)
    data[0] = time.time() - start
    write = "%d,%d,%d,%d,%d,%d\n" % (data[0], data[1], data[2], data[3], data[4], data[5])
    f.write(write)

    cv2.imshow('window', img_gray)
    if cv2.waitKey(25) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        f.close()
        break     