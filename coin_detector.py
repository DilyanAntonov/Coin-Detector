import cv2
import numpy as np
import matplotlib.pyplot as plt


def image_processing(img_path):
    def nothing(x):
        pass

    def filter_image(img_path: str, scale_percent: int, rotate_img: bool):
        """ Getting, resizing and filtering the image """

        img = cv2.imread(img_path)
        if rotate_img == True:
            img = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
        else:
            pass
        filter_image.img = img.copy()
        height = int(img.shape[0] * scale_percent / 100)
        width = int(img.shape[1] * scale_percent / 100)
        dimetions = (width, height)
        filter_image.resized_img = cv2.resize(img, dimetions, interpolation=cv2.INTER_AREA)
        gray = cv2.cvtColor(filter_image.resized_img, cv2.COLOR_BGR2GRAY)
        filter_image.blurred_img = cv2.GaussianBlur(gray, (3, 199), cv2.BORDER_DEFAULT)

        return True

    def detect_coins(coins, img, value_of_coin, currency):
        """ Detects and draws the circles on the image.
        Prints the number of the detected coins """
        

        if coins is not None:
            # ===== Casting to normal ints =====
            detected_coins = np.uint16(np.round(coins))
            
            # ===== Drawing the circles =====
            for coin in np.asarray(detected_coins[0, :]):
                cv2.circle(filter_image.resized_img, (coin[0], coin[1]), coin[2], (0, 255, 0), 2)
                cv2.circle(filter_image.resized_img, (coin[0], coin[1]), 2, (255, 000, 0), 3)

            x = [(len(i)) for i in detected_coins]
            print("You have {value} {currency}".format(value=value_of_coin*x[0], currency=currency))

        else:
            print("You have no coins :(")
            
        return True
        
    # ===== Creating the windows =====
    cv2.namedWindow("Coin Detection")
    cv2.createTrackbar("param1_slider", "Coin Detection", 50, 255, nothing)
    cv2.createTrackbar("param2_slider", "Coin Detection", 30, 255, nothing)
    cv2.createTrackbar("min_rad_slider", "Coin Detection", 0, 255, nothing)
    cv2.createTrackbar("max_rad_slider", "Coin Detection", 90, 255, nothing)

    while True:
        filter_image(img_path, 30, True)

        # ===== Keeps constant track of the sliders =====
        param1_slider_value = int(cv2.getTrackbarPos("param1_slider", "Coin Detection"))
        param2_slider_value = int(cv2.getTrackbarPos("param2_slider", "Coin Detection"))
        param1_lastvalue = 0
        param2_lastvalue = 0

        min_rad_slider_value = int(cv2.getTrackbarPos("min_rad_slider", "Coin Detection"))
        max_rad_slider_value = int(cv2.getTrackbarPos("max_rad_slider", "Coin Detection"))
        min_rad_lastvalue = 0
        max_rad_lastvalue = 0

        # ===== Edge Cases =====
        """ There is no way to set a minimum in the slider, but
        if the value goes to 0 the HoughCircle function breaks """

        if param1_lastvalue != param1_slider_value:
            if param1_slider_value <= 3:
                param1_slider_value = 10
                cv2.createTrackbar("param1_slider", "Coin Detection", 10, 255, nothing)
            else:
                param1_lastvalue = param1_slider_value
                cv2.imshow("Coin Detection", filter_image.resized_img)
                
        if param2_lastvalue != param2_slider_value:
            if param2_slider_value <= 3:
                param2_slider_value = 10
                cv2.createTrackbar("param2_slider", "Coin Detection", 10, 255, nothing)
            else:
                param2_lastvalue = param2_slider_value
                cv2.imshow("Coin Detection", filter_image.resized_img)
        
        if min_rad_lastvalue != min_rad_slider_value:
            min_rad_lastvalue = min_rad_slider_value
            cv2.imshow("Coin Detection", filter_image.resized_img)

        if max_rad_lastvalue != max_rad_slider_value:
            # if max_rad_slider_value <= 3:
            #     max_rad_slider_value = 4
            #     cv2.createTrackbar("max_rad_slider", "Coin Detection", 90, 255, nothing)
            # else:
                max_rad_lastvalue = max_rad_slider_value
                cv2.imshow("Coin Detection", filter_image.resized_img)

        coins = cv2.HoughCircles(filter_image.blurred_img , cv2.HOUGH_GRADIENT, 1, 20, param1=int(param1_slider_value),
                                param2=int(param2_slider_value),
                                minRadius=int(min_rad_slider_value), maxRadius=int(max_rad_slider_value))

        detect_coins(coins, filter_image.resized_img, 2, "BGN")

        cv2.imshow("Coin Detection", filter_image.resized_img)
        key = cv2.waitKey(1)
        if key == 27:
            break