import cv2
import numpy as np
import matplotlib.pyplot as plt


def nothing(x):
    pass

# ===== Filtering the image =====
img_path = "img/4_coins.jpg"
img = cv2.imread(img_path, 1)
img_orig = img.copy()
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
blurred_img = cv2.GaussianBlur(gray, (21, 21), cv2.BORDER_DEFAULT)


# ===== Creating the windows =====
cv2.namedWindow("Coin Detection")
cv2.createTrackbar("param1_slider", "Coin Detection", 50, 60, nothing)
cv2.createTrackbar("param2_slider", "Coin Detection", 30, 60, nothing)

while True:
    # ===== Keeps constant track of the sliders =====
    param1_slider_value = int(cv2.getTrackbarPos("param1_slider", "Coin Detection"))
    param2_slider_value = int(cv2.getTrackbarPos("param2_slider", "Coin Detection"))
    param1_lastvalue = 0
    param2_lastvalue = 0

    if param1_lastvalue != param1_slider_value:
        param1_lastvalue = param1_slider_value
        img_orig = cv2.imread(img_path, 1)
        cv2.imshow("Coin Detection", img_orig)

    # ===== Edge Cases =====
    """ There is no way to set a minimum in the slider, but
        if the value goes to 0 the HoughCircle function breaks"""
    if param2_lastvalue != param2_slider_value:
        if param2_slider_value <= 5:
            param2_slider_value = 30
            cv2.createTrackbar("param2_slider", "Coin Detection", 30, 60, nothing)
        else:
            param2_lastvalue = param2_slider_value
            img_orig = cv2.imread(img_path, 1)
            cv2.imshow("Coin Detection", img_orig)

        if param1_slider_value <= 5:
            param1_slider_value = 50
            cv2.createTrackbar("param1_slider", "Coin Detection", 50, 60, nothing)
        else:
            param1_lastvalue = param2_slider_value
            img_orig = cv2.imread(img_path, 1)
            cv2.imshow("Coin Detection", img_orig)

        all_coins = cv2.HoughCircles(blurred_img, cv2.HOUGH_GRADIENT, 1, 20, param1=int(param1_slider_value),
                                     param2=int(param2_slider_value),
                                     minRadius=0, maxRadius=0)

        if all_coins is not None:
            # ===== Casting to normal ints =====
            detected_coins = np.uint16(np.round(all_coins))

            # ===== Drawing the circles =====
            for coin in np.asarray(detected_coins[0, :]):
                cv2.circle(img_orig, (coin[0], coin[1]), coin[2], (0, 255, 0), 3)
                cv2.circle(img_orig, (coin[0], coin[1]), 2, (255, 000, 0), 3)

            x = [(len(i)) for i in detected_coins]
            print("You have {} coins!".format(x[0]))
        else:
            print("You have 0 coins!")




    cv2.imshow("Coin Detection", img_orig)

    key = cv2.waitKey(1)
    if key == 27:
        break
