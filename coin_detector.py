import cv2
import numpy as np
import matplotlib.pyplot as plt


def nothing(x):
    pass

def filter_image(img_path: str, scale_percent: int):
    """ Getting, resizing and filtering the image """

    img = cv2.imread(img_path)
    filter_image.img_orig = img.copy()
    height = int(img.shape[0] * scale_percent / 100)
    width = int(img.shape[1] * scale_percent / 100)
    dimetions = (width, height)
    filter_image.resized_img = cv2.resize(img, dimetions, interpolation=cv2.INTER_AREA)
    gray = cv2.cvtColor(filter_image.resized_img, cv2.COLOR_BGR2GRAY)
    filter_image.blurred_img = cv2.GaussianBlur(gray, (21, 21), cv2.BORDER_DEFAULT)

    return True

def detect_coins(coins, img):
    """ Detects and draws the circles on the image.
       Prints the number of the detected coins """
    if coins is not None:
        # ===== Casting to normal ints =====
        detected_coins = np.uint16(np.round(coins))

        # ===== Drawing the circles =====
        for coin in np.asarray(detected_coins[0, :]):
            cv2.circle(filter_image.resized_img, (coin[0], coin[1]), coin[2], (0, 255, 0), 3)
            cv2.circle(filter_image.resized_img, (coin[0], coin[1]), 2, (255, 000, 0), 3)

        x = [(len(i)) for i in detected_coins]
        print("You have {} coins!".format(x[0]))

    else:
        print("You have 0 coins!")
        
    return True
    
# ===== Creating the windows =====
cv2.namedWindow("Coin Detection")
cv2.createTrackbar("param1_slider", "Coin Detection", 50, 255, nothing)
cv2.createTrackbar("param2_slider", "Coin Detection", 30, 255, nothing)

while True:
    filter_image("img/13_coins.jpg", 90)

    # ===== Keeps constant track of the sliders =====
    param1_slider_value = int(cv2.getTrackbarPos("param1_slider", "Coin Detection"))
    param2_slider_value = int(cv2.getTrackbarPos("param2_slider", "Coin Detection"))
    param1_lastvalue = 0
    param2_lastvalue = 0

    # ===== Edge Cases =====
    """ There is no way to set a minimum in the slider, but
    if the value goes to 0 the HoughCircle function breaks """

    if param1_lastvalue != param1_slider_value:
        param1_lastvalue = param1_slider_value
        cv2.imshow("Coin Detection", filter_image.resized_img)

        if param1_slider_value <= 10:
            param1_slider_value = 50
            cv2.createTrackbar("param1_slider", "Coin Detection", 50, 255, nothing)
        else:
            param1_lastvalue = param1_slider_value
            cv2.imshow("Coin Detection", filter_image.resized_img)
            
    if param2_lastvalue != param2_slider_value:
        if param2_slider_value <= 10:
            param2_slider_value = 30
            cv2.createTrackbar("param2_slider", "Coin Detection", 30, 255, nothing)
        else:
            param2_lastvalue = param2_slider_value
            cv2.imshow("Coin Detection", filter_image.resized_img)

    coins = cv2.HoughCircles(filter_image.blurred_img , cv2.HOUGH_GRADIENT, 1, 20, param1=int(param1_slider_value),
                            param2=int(param2_slider_value),
                            minRadius=0, maxRadius=0)

    detect_coins(coins, filter_image.resized_img)

    cv2.imshow("Coin Detection", filter_image.resized_img)
    key = cv2.waitKey(1)
    if key == 27:
        break