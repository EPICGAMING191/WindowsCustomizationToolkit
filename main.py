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
global batteryLifeText_

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

def update(args):
    print(args + "hi")
    #text_.set(text="Battery Life: " + str(get_battery_percent()) + "%")
    app.after(10, update, 1)
    print(args)
    


def update_slider():
    slider_.set(getScreenBrightness())
    app.after(10, update_slider)

def label(text_, x = 20, y = 20, width_= 40, height_= 40, text_size = 15):
    thislabel =  ctk.CTkLabel(app, text=text_, width=width_, height=height_, font=("Arial", text_size, 'bold'), bg_color="transparent", text_color="white")
    thislabel.place(x=x, y=y)
    return thislabel

def setupRoot(width_, height_):
    ctk.set_appearance_mode('dark')
    app.title("Windows Customization Toolkit")
    app.geometry(f"{width_}x{height_}")
    app.resizable(False, False)

def get_battery_percent():
    return psutil.sensors_battery()[0]

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
    slider1(10, 60)
    label("Windows Customization Toolkit", x=0, y=10, text_size=25, width_=1100)
    label("Screen Brightness", x=15, y=20)
    batteryLifeText_ = label("Battery Life: " + str(get_battery_percent()) + "%", x=970, y=0)
    app.after(10, update_slider)
    app.after(10, update, batteryLifeText_)
    app.mainloop()
input()