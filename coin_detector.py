from tkinter import *
import cv2
from PIL import Image, ImageTk
from tkinter import filedialog
from functions import *


def select_image():
    """Selects the image. Used as a command on a button."""

    select_image.path = filedialog.askopenfilename(filetypes=[("Image File",'.jpg')])
    select_image.img = Image.open(select_image.path)
    select_image.tkimage = ImageTk.PhotoImage(select_image.img)
    return select_image.path

window = Tk()  
window.geometry("500x250")  
window.title("Coin Detection")
font = ("Courier", 20)


# ===== Labels =====
label1 = Label(window, text="Worth of a coin ")
label1.config(font=font)
label1.grid(row=1, column=0)

label2 = Label(window, text="Scale ")
label2.config(font=font)
label2.grid(row=2, column=0)

label3 = Label(window, text="Flip Image ")
label3.config(font=font)
label3.grid(row=3, column=0)


# ===== Dropdown Menus =====
value_options = ["1", "2", "0.50", "0.25", "0.20", "0.10", "0.05", "0.02", "0.01"]
currency_options = ["EUR", "USD", "BGN", "JPY"]
scale_options = ["90%", "80%", "70%", "60%", "50%", "40%", "30%", "20%", "10%"]
flip_options = ["Yes", "No"]

value_first_option = StringVar(window) # Used to retrieve the selected value
value_first_option.set(value_options[0])

currency_first_option = StringVar(window) # Used to retrieve the selected value
currency_first_option.set(currency_options[0])

scale_first_option = StringVar(window) # Used to retrieve the selected value
scale_first_option.set(scale_options[5])

flip_first_option = StringVar(window)
flip_first_option.set(flip_options[0])


value_dropdown = OptionMenu(window, value_first_option, *value_options)
value_dropdown.config(width=3, font=font)
value_dropdown.grid(row=1, column=1)

currency_dropdown = OptionMenu(window, currency_first_option, *currency_options)
currency_dropdown.config(width=3, font=font)
currency_dropdown.grid(row=1, column=2)

scale_dropdown = OptionMenu(window, scale_first_option, *scale_options)
scale_dropdown.config(width=3, font=font)
scale_dropdown.grid(row=2, column=1)

flip_dropdown = OptionMenu(window, flip_first_option, *flip_options)
flip_dropdown.config(width=3, font=font)
flip_dropdown.grid(row=3, column=1)


# ===== Buttons =====
button1 = Button(window, text = "Calculate", command = lambda: image_processing(img_path=select_image.path,
                                                                                value=float(value_first_option.get()),
                                                                                currency=currency_first_option.get(),
                                                                                scale=int(scale_first_option.get()[0:2]),
                                                                                flip=str(flip_first_option.get())))
                                                
button1.config(width=13, font=font)
button1.grid(row=5, column=0)

button2 = Button(window, text = "Select Image", command = select_image)
button2.config(width=13, font=font)
button2.grid(row=4, column=0)

window.mainloop()