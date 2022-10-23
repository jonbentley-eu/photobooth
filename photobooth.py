from time import sleep
from datetime import datetime
from sh import gphoto2 as gp
import signal, os, subprocess
import RPi.GPIO as GPIO


#setup GPIO, change pin as required.
GPIO.setmode(GPIO.BOARD)
btn_pin = 33
GPIO.setup(btn_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
buttonPressedTime = None

#setup gphoto2


#kill gphoto2 process that starts whenever we connect the camera
def killgphoto2Process ():
    p = subprocess.Popen(['ps', '-A'], stdout=subprocess.PIPE)
    out, err = p.communicate()
    
# Search for the line that has the process we want to kill
    for line in out.splitlines():
        if b'gvfsd-gphoto2' in line:
            #kill the process!
            pid = int(line.split(None,1) [0])
            os.kill(pid, signal.SIGKILL)

shot_date = datetime.now().strftime ("%Y-%m-%d")
shot_time = datetime.now().strftime ("%Y-%m-%d %H:%M:%S")

triggerCommand = ["--capture-image"]


def captureImages():
    gp(triggerCommand)
    sleep(3)

#countdown
def countdown(n):
    if n == 0:
        print ("Smile!!") 
    else:
        sleep(2)
        print(n)
        countdown(n-1)

#detect the button being pressed
def buttonStateChanged(pin):
    global buttonPressedTime
    
    if not (GPIO.input(pin)):
        if buttonPressedTime is None:
            buttonPressedTime = datetime.now()
            print ('Button Pressed')
    
    else:
        if buttonPressedTime is not None:
            countdown (3)
            killgphoto2Process()
            captureImages()
            sleep(1)
            killgphoto2Process()
            captureImages()
            buttonPressedTime = None



#read button
GPIO.add_event_detect(btn_pin, GPIO.BOTH, callback=buttonStateChanged)

while True:
    sleep(5)
