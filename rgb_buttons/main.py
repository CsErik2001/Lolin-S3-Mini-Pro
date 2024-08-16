from machine import Pin
from time import sleep
from neopixel import NeoPixel

# Set up the RGB LED power pin
power_pin = Pin(7, Pin.OUT)
power_pin.value(1)  # Ensure the RGB LED is powered

# Set up the RGB LED data pin
led_pin = Pin(8, Pin.OUT)
np = NeoPixel(led_pin, 1)

# Set up the buttons
button1 = Pin(0, Pin.IN, Pin.PULL_UP)
button2 = Pin(47, Pin.IN, Pin.PULL_UP)
button3 = Pin(48, Pin.IN, Pin.PULL_UP)

while True:
    if not button1.value():  # Button 1 pressed
        np[0] = (0, 0, 255)  # Red
        np.write()
        print("Button 1 pressed: Red")

    elif not button2.value():  # Button 2 pressed
        np[0] = (0, 255, 0)  # Green
        np.write()
        print("Button 2 pressed: Green")

    elif not button3.value():  # Button 3 pressed
        np[0] = (255, 0, 0)  # Blue
        np.write()
        print("Button 3 pressed: Blue")

    sleep(0.1)  # Debounce delay
