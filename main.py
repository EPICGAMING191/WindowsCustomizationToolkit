import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
from screeninfo import get_monitors
import screen_brightness_control as sbc
import threading
import psutil
import platform

global slider_
global brightness
global sideFrame
global dropdown_
global batteryLifeText_

app = ctk.CTk()
width = 1100
height = 580

def setScreenBrightness(brightness):
    sbc.set_brightness(brightness)

def get_battery_percent():
    return psutil.sensors_battery()[0]

def is_battery_plugged_in():
    return psutil.sensors_battery().power_plugged
    
def getScreenBrightness():
    return sbc.get_brightness()[0]

def update(text_):
    if(is_battery_plugged_in()):
        pluggedInText = " (Plugged In)"
        text_.place(x=870, y=0)
    else:
        pluggedInText = ""
        text_.place(x=970, y=0)
        
    text_.configure(text="Battery Life: " + str(get_battery_percent()) + "%" + pluggedInText)
    if(get_battery_percent() > 50):
        text_.configure(text_color="green")
    elif(get_battery_percent() >= 20):
        text_.configure(text_color="yellow")
    else:
        text_.configure(text_color="red")
    app.after(10, update, text_)

def isPasswordCorrect(pwd):
    passwords = ['guest', 'user1', 'user2', 'user3']
    for str in passwords:
        if(pwd == str):
            return True
    return False    

def update_slider():
    slider_.set(getScreenBrightness())
    app.after(10, update_slider)

def label(text_, x = 20, y = 20, width_= 40, height_= 40, text_size = 15, text_color_ = 'white'):
    thislabel =  ctk.CTkLabel(app, text=text_, width=width_, height=height_, font=("Arial", text_size, 'bold'), bg_color="transparent", text_color=text_color_)
    thislabel.place(x=x, y=y)
    return thislabel

def inputDialog(title_, text_):
    dialog = ctk.CTkInputDialog(text=text_, title=title_)
    return dialog.get_input()

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

if __name__ == '__main__':
    setupRoot(width, height)
    slider1(10, 60)
    pwd = inputDialog("Enter password: ", "Enter password here: ")
    while(not isPasswordCorrect(pwd)):
        pwd = inputDialog("incorrect password: ", "Enter password here: ")
        if(pwd.lower() =="cancel"):
            exit(1)
    label("Windows Customization Toolkit", x=0, y=10, text_size=25, width_=1100)
    label("Screen Brightness", x=15, y=20)
    batteryLifeText_ = label("Battery Life: " + str(get_battery_percent()) + "%", x=970, y=0)
    app.after(10, update_slider)
    app.after(10, update, batteryLifeText_)
    app.mainloop()

input()