import ac
import acsys
import os
import configparser

# Global variables
brake_threshold = 0.2
gas_threshold = 0.2
timer = 0.0
beep_active = False
red_circle = None

def acMain(ac_version):
    global threshold, red_circle
    
    appWindow = ac.newApp("BSPD_Alert")
    ac.setSize(appWindow, 100, 100)
    ac.drawBorder(appWindow, 0)
    ac.setBackgroundOpacity(appWindow, 0)
    
    # Create the "Red Circle" using a label with a background color
    red_circle = ac.addLabel(appWindow, "")
    ac.setSize(red_circle, 50, 50)
    ac.setPosition(red_circle, 25, 25)
    ac.setBackgroundColor(red_circle, 1, 0, 0) # Red
    ac.setVisible(red_circle, 0) # Start hidden

    # Load threshold from config.txt
    try:
        # Get path to the app folder
        config = configparser.ConfigParser()
        config.read("config.ini")
        brake_threshold = config.getfloat('THRESHOLDS', 'brake_threshold')
        gas_threshold = config.getfloat('THRESHOLDS', 'gas_threshold')
        timer_threshold = config.getfloat('THRESHOLDS', 'timer_threshold')

    except:
        ac.log("BSPD_Alert: Could not read config.ini, using default")

    return "BSPD_Alert"

def acUpdate(delta_t):
    global timer, threshold, red_circle

    # Get pedal states (0.0 to 1.0)
    gas = ac.getCarState(0, acsys.CS.Gas)
    brake = ac.getCarState(0, acsys.CS.Brake)

    # Check if both are above threshold
    if gas > threshold and brake > threshold:
        timer += delta_t
    else:
        timer = 0
        ac.setVisible(red_circle, 0)

    # Trigger if held for more than 0.5 seconds
    if timer > 0.5:
        ac.setVisible(red_circle, 1)
        # Note: AC Python API doesn't have a native 'beep' function.
        # Most modders use the 'winsound' library (Windows only) 
        # or play a short .wav via a hidden invisible audio entity.
        import winsound
        winsound.Beep(1000, 100) # 1000Hz for 100ms