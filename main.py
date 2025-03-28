#Documentation used: https://customtkinter.tomschimansky.com/

from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL

from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
from screeninfo import get_monitors
import screen_brightness_control as sbc
import psutil
        

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


def set_volume(vol):
    try:
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = cast(interface, POINTER(IAudioEndpointVolume))
        volume.SetMasterVolumeLevelScalar(vol / 100, None)    
    except:
        return    

def get_volume():
    try:
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = interface.QueryInterface(IAudioEndpointVolume)
        return int(volume.GetMasterVolumeLevelScalar() * 100)  # Convert to percentage
    except:
        return -1
 

def get_battery_percent():
    return psutil.sensors_battery()[0]

def is_battery_plugged_in():
    return psutil.sensors_battery().power_plugged
    
def getScreenBrightness():
    return sbc.get_brightness()[0]

def getCPU():
    return psutil.cpu_percent()

def getRam():
    return psutil.virtual_memory().percent

def login(pwd_):
    if(pwd_ == None):
        exit(1)
    while(not isPasswordCorrect(pwd_)[0]):
        pwd_ = inputDialog("Incorrect password! ", "Enter password here: ")
        if(pwd_ is not None):
            if(pwd_.lower() =="cancel"):
                exit(1)
        else:
            exit(1)        


def update(text_, cpu_, ram_):
    cpuPercent = getCPU()
    ramPercent = getRam()
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
    if(ramPercent < 50):
        ram_.configure(text_color="green")
    elif(ramPercent <= 85):
        ram_.configure(text_color="yellow")
    else:
        ram_.configure(text_color="red")

    if(cpuPercent < 50):
        cpu_.configure(text_color="green")
    elif(cpuPercent <= 85):
        cpu_.configure(text_color="yellow")
    else:
        cpu_.configure(text_color="red")

    cpu_.configure(text="CPU Usage: " + str(cpuPercent) + "%")   
    ram_.configure(text="RAM Usage: " + str(ramPercent) + "%")   
    app.after(1000, update, text_, cpu_, ram_)

def update_100ms(volumeLabel_, screenBrightnessLabel_):
    if(get_volume() != -1):
        volumeLabel_.configure(text="Volume: " + str(get_volume()) + "%") 
    else:
        volumeLabel_.configure(text="Volume: DISABLED")  
    screenBrightnessLabel_.configure(text="Screen Brightness: " + str(getScreenBrightness()) + "%")
    app.after(100, update_100ms, volumeLabel_, screenBrightnessLabel_)    

def isPasswordCorrect(pwd):
    passwords = ['guest', 'user1', 'user2', 'user3']
    for str_ in passwords:
        if(pwd == str_):
            return True, str_
    return False, None    

def update_slider(vol_, warned):
    if(get_volume() == -1):
        volumeSlider.configure(state="disabled")
        if(warned):
            app.after(10, update_slider, vol_, True)
        else:
            CTkMessagebox(title="Error", message="No audio output devices found.", icon="cancel")  
            app.after(10, update_slider, vol_, True)
    else:    
        slider_.set(getScreenBrightness())
        vol_.set(get_volume())
        app.after(10, update_slider, vol_, True)

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


def slider1(x_, y_, command_, setValue_, from_=0, to_=100,):
    global slider_
    slider_ = ctk.CTkSlider(app, from_=from_, to=to_, command=command_, bg_color="transparent", fg_color="black")
    slider_.set(setValue_)
    slider_.place(x=x_, y=y_)
    return slider_

if __name__ == '__main__':
    setupRoot(width, height)
    slider1(10, 60, setScreenBrightness, getScreenBrightness())
    volumeSlider = slider1(10, 220, set_volume, get_volume())
    pwd = inputDialog("Enter password: ", "Enter password here: ")
    login(pwd)
    title = label("Windows Customization Toolkit", x=0, y=10, text_size=25, width_=1100)
    screenBrightnessLabel = label("Screen Brightness: " + str(getScreenBrightness()) + "%", x=15, y=20)
    batteryLifeText_ = label("Battery Life: " + str(get_battery_percent()) + "%", x=970, y=0)
    volumeLabel = label("Volume: " + str(get_volume()) + "%", x=15, y=180)
    cpu = label("CPU Usage: 0%", x=15, y=100)
    ram = label("RAM Usage: 0%", x=15, y=140)
    app.after(10, update_slider, volumeSlider, False)
    app.after(10, update, batteryLifeText_, cpu, ram)
    app.after(10, update_100ms, volumeLabel, screenBrightnessLabel)
    app.mainloop()

input()