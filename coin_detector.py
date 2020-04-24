import cv2
import numpy as np
import matplotlib.pyplot as plt

img = cv2.imread('img/13_coins.jpg', 1)
img_orig = img.copy()
img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
img = cv2.GaussianBlur(img, (21, 21), cv2.BORDER_DEFAULT)

all_coins = cv2.HoughCircles(img, cv2.HOUGH_GRADIENT, 1, 20, param1=30, param2=15,
                        minRadius=0, maxRadius=0)

detected_coins = np.uint16(np.round(all_coins))

for coin in detected_coins[0, :]:
    cv2.circle(img_orig, (coin[0], coin[1]), coin[2], (0, 255, 0), 3)
    cv2.circle(img_orig, (coin[0], coin[1]), 2, (255, 000, 0), 3)


x = [(len(i)) for i in detected_coins]
print("You have {} coins!".format(x[0]))



cv2.imshow("Coin Detection", img_orig)
cv2.waitKey(0)
cv2.destroyAllWindows()
