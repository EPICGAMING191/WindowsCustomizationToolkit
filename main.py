import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
from screeninfo import get_monitors
import screen_brightness_control as sbc
import threading
import psutil

themes = ['Dark', 'Light']

global slider_
global brightness
global sideFrame
global dropdown_

app = ctk.CTk()
try:
    width = 1100
    height = 580
except:
    messagebox = CTkMessagebox(title="Error", message="No displays available.")
    exit(0)


def setScreenBrightness(brightness):
    sbc.set_brightness(brightness)
    
    
def getScreenBrightness():
    return sbc.get_brightness()[0]

def update(*args):
    global dropdown_
    app._set_appearance_mode(dropdown_.get())
    app.update_idletasks()


def frame():
    global sideFrame

def update_slider():
    slider_.set(getScreenBrightness())
    app.after(10, update_slider)

def label(text_, x = 20, y = 20, width_= 40, height_= 40, text_size = 15):
    ctk.CTkLabel(app, text=text_, width=width_, height=height_, font=("Arial", text_size, 'bold'), bg_color="transparent", text_color="white").place(x=x, y=y)

def setupRoot(width_, height_):
    ctk.set_appearance_mode('dark')
    app.title("Windows Customization Toolkit")
    app.geometry(f"{width_}x{height_}")
    app.resizable(False, False)

def slider1(x_, y_):
    global slider_
    slider_ = ctk.CTkSlider(app, from_=0, to=100, command=setScreenBrightness, bg_color="transparent", fg_color="black")
    slider_.set(getScreenBrightness())
    slider_.place(x=x_, y=y_)

def dropdown(x_, y_):
    global dropdown_
    dropdown_ = ctk.CTkOptionMenu(app, values=themes, command=update)
    dropdown_.set(themes[0])
    dropdown_.place(x=x_, y=y_)


if __name__ == '__main__':
    setupRoot(width, height)
    frame()
    slider1(10, 60)
    label("Windows Customization Toolkit", x=0, y=10, text_size=25, width_=1100)
    label("Screen Brightness", x=15, y=20)
    app.after(10, update_slider)
    app.mainloop()
input()