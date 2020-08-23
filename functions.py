import cv2
import numpy as np


def image_processing(img_path: str, value: float, currency: str, scale: int, flip="Yes"):
    """ 
    Contains the whole 'backend' of the program. Directly called in the coin_detector.py file (GUI)
    
    Parameters:
    img_path (str): The path to the image file. Selected from the GUI

    value (float): The value of the coin. Selected from the GUI

    currency (str): The name of the currency of the coins. Selected from the GUI

    scale (str): The scale to shrink the image. Selected from the GUI

    flip (str): Shows if the image has to be flipped horizontally 90 degrees or not. Selected from the GUI
    """

    def nothing():
        '''
        Needed for the createTrackbar function from OpenCV
        '''
        pass
    

    def filter_image(img_path: str, flip_img=flip):
        """ 
        Obtaining, resizing and filtering the image

        Parameters:
        img_path (str): The path to the image file.

        flip_img (str): Uses the flip parameter from the image_processing() function
        """

        img = cv2.imread(img_path)

        if flip_img == "Yes":
            img = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
        else:
            pass

        filter_image.img = img.copy()
        height = int(img.shape[0] * scale / 100)
        width = int(img.shape[1] * scale / 100)
        dimetions = (width, height)
        filter_image.resized_img = cv2.resize(img, dimetions, interpolation=cv2.INTER_AREA)
        gray = cv2.cvtColor(filter_image.resized_img, cv2.COLOR_BGR2GRAY)
        filter_image.blurred_img = cv2.GaussianBlur(gray, (3, 199), cv2.BORDER_DEFAULT)

        return True


    def detect_coins(coins, img, value_of_coin, currency):
        """ 
        Detects the circles on the image.
        Shows each one individually with a green outline.
        Shows in the popup window the amount of coins detected and their currency.

        Parameters:
        coins (numpy.ndarray): Created using the HoughCircles function from OpenCV. 
                               Contains the data for each detected coins.
        
        img (function): Contains the processed image from the filter_image() function.

        value_of_coin (float): Contains the value of each coin.

        currency (str): Contains the currency of the coins.
        """
        
        font = cv2.FONT_HERSHEY_SIMPLEX

        if coins is not None:
            # ===== Casting to normal ints =====
            detected_coins = np.uint16(np.round(coins))
            
            # ===== Drawing the circles =====
            for coin in np.asarray(detected_coins[0, :]):
                cv2.circle(filter_image.resized_img, (coin[0], coin[1]), coin[2], (0, 255, 0), 2)
                cv2.circle(filter_image.resized_img, (coin[0], coin[1]), 2, (255, 000, 0), 3)
            
            x = [(len(i)) for i in detected_coins]

            cv2.putText(img, "You have {value} {currency}".format(value=int(value_of_coin*x[0]), currency=currency), 
                                                                                (int(img.shape[1] - (img.shape[1]-10)), int(img.shape[0] - (img.shape[0]-30))), 
                                                                                    font, 1, (0, 255, 0), 3, cv2.LINE_AA)
        else:
            cv2.putText(img, "You have 0 {currency}".format(currency=currency), (int(img.shape[1] - (img.shape[1]-10)), int(img.shape[0] - (img.shape[0]-30))), 
                                                                                    font, 1, (0, 255, 0), 3, cv2.LINE_AA)      
        return True
        
    # ===== Creating the windows =====
    cv2.namedWindow("Coin Detection")
    cv2.createTrackbar("param1_slider", "Coin Detection", 50, 255, nothing)
    cv2.createTrackbar("param2_slider", "Coin Detection", 30, 255, nothing)
    cv2.createTrackbar("min_rad_slider", "Coin Detection", 0, 255, nothing)
    cv2.createTrackbar("max_rad_slider", "Coin Detection", 90, 255, nothing)

    while True:
        filter_image(img_path, flip)

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
                max_rad_lastvalue = max_rad_slider_value
                cv2.imshow("Coin Detection", filter_image.resized_img)

        coins = cv2.HoughCircles(filter_image.blurred_img , cv2.HOUGH_GRADIENT, 1, 20, param1=int(param1_slider_value),
                                param2=int(param2_slider_value),
                                minRadius=int(min_rad_slider_value), maxRadius=int(max_rad_slider_value))

        detect_coins(coins, filter_image.resized_img, value, currency)

        cv2.imshow("Coin Detection", filter_image.resized_img)
        key = cv2.waitKey(1)
        if key == 27:
            break