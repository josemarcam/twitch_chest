import numpy as np
import cv2
import os 
import pyautogui
import imutils
import time
def get_image_rgb_hsv(image_path):
    image = cv2.imread(image_path)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image_hsv = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)
    return image_rgb,image_hsv
def seach_chest(image_path):
    image_rgb,image_hsv = get_image_rgb_hsv(image_path)
    height, width, channels = image_rgb.shape
    h = round(height*0.75)
    w = round(width*0.75)
    lower = np.array([0,229,204])
    upper = np.array([0,230,205])

    crop_rgb = image_rgb[h:,w:]
    mask = cv2.inRange(image_rgb,lower,upper)
    thresh = cv2.threshold(mask, 45, 255, cv2.THRESH_BINARY)[1]
    thresh = cv2.erode(thresh, None, iterations=2)
    thresh = cv2.dilate(thresh, None, iterations=2)
    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    if not cnts:
        return np.array([])
    c = max(cnts, key=cv2.contourArea)
    return c

while True:
    myScreenshot = pyautogui.screenshot()
    myScreenshot.save(r'./cap5.png')
    c = seach_chest("cap5.png")
    if c.any():
        M = cv2.moments(c)
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
        if (cY > 200):
            print("bau encontrado!")
            atualX,atualY = pyautogui.position()
            pyautogui.moveTo(cX,cY,0.05)
            pyautogui.click()
            pyautogui.moveTo(atualX,atualY,0.05)
    os.remove("cap5.png")
    time.sleep(3)






