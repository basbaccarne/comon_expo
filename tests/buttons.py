# This script reads the state of three buttons connected to GPIO pins 4, 14 and 25

from time import sleep
from gpiozero import Button
from sys import exit

# buttons are connected to ground and pins 4, 14 and 25
button1 = Button(4)
button2 = Button(14)
button3 = Button(25)

# set debouce parameter
debounce = 0.3

print("ready to go ...")

try:
    while True:
        if button1.is_pressed:
            print("Button 1 pressed")
            sleep(debounce)  # Debounce delay to prevent multiple triggers
        if button2.is_pressed:
            print("Button 2 pressed")
            sleep(debounce)
        if button3.is_pressed:
            print("Button 3 pressed")
            sleep(debounce)
except KeyboardInterrupt:
    print("\nThis was fun, see you next time ...")
    exit()