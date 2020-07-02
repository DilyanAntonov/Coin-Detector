from tkinter import *
import cv2
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image, ImageTk
from tkinter import filedialog
from coin_detector import image_processing

window = Tk()  # The main tkinter function
window.geometry("900x600")  # Setting the size of the window
window.title("Coin Detection")
font = ("Courier", 20)

label1 = Label(window, text="Worth of a coin:")
label1.config(font=font)
label1.grid(row=1, column=0)

value_options = ["1", "2", "0.50", "0.20", "0.10", "0.05", "0.02", "0.01"]
currency_options = ["EUR", "USD", "BGN", "JPY"]

value_first_option = StringVar(window)
value_first_option.set(value_options[0])

value_dropdown = OptionMenu(window, value_first_option, *value_options)
value_dropdown.config(width=3, font=font)
value_dropdown.grid(row=1, column=1)

currency_first_option = StringVar(window)
currency_first_option.set(currency_options[0])

currency_dropdown = OptionMenu(window, currency_first_option, *currency_options)
currency_dropdown.config(width=3, font=font)
currency_dropdown.grid(row=1, column=2)

def select_image():
    select_image.path = filedialog.askopenfilename(filetypes=[("Image File",'.jpg')])
    select_image.img = Image.open(select_image.path)
    select_image.tkimage = ImageTk.PhotoImage(select_image.img)
    return select_image.path

def callback(amount):
    value = float(value_first_option.get())
    currency = currency_first_option.get()
    
    text = "You have {value} {currency}".format(value=value*amount, currency=currency)
    print(text)
    return text

button1 = Button(window, text = "Calculate", command = lambda: image_processing(select_image.path))
button1.config(width=9, font=font)
button1.grid(row=2, column=0)

button2 = Button(window, text = "Select Image", command = select_image)
button2.config(width=13, font=font)
button2.grid(row=3, column=0)

window.mainloop()