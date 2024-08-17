# Import necessary modules from the helper library
from time import sleep
import s3minipro as helper  # Replace 's3minipro' with the actual filename

# Ensure RGB LED power is enabled
power_pin = Pin(helper.RGB_POWER, Pin.OUT)
power_pin.value(1)  # Turn on the RGB LED power

while True:
    # Check for all possible combinations of button presses
    if not helper.button0.value() and not helper.button47.value() and not helper.button48.value():  # All three buttons pressed
        helper.rgb_led(255, 255, 255)  # White (Red + Green + Blue)
        print("Button 0 (Blue), Button 47 (Red), and Button 48 (Green) pressed: White")

    elif not helper.button0.value() and not helper.button47.value():  # Blue and Red buttons pressed together
        helper.rgb_led(255, 0, 255)  # Magenta (Red + Blue)
        print("Button 0 (Blue) and Button 47 (Red) pressed: Magenta")

    elif not helper.button0.value() and not helper.button48.value():  # Blue and Green buttons pressed together
        helper.rgb_led(0, 255, 255)  # Cyan (Green + Blue)
        print("Button 0 (Blue) and Button 48 (Green) pressed: Cyan")

    elif not helper.button47.value() and not helper.button48.value():  # Red and Green buttons pressed together
        helper.rgb_led(255, 255, 0)  # Yellow (Red + Green)
        print("Button 47 (Red) and Button 48 (Green) pressed: Yellow")

    elif not helper.button0.value():  # Button 0 pressed (Blue)
        helper.rgb_led(0, 0, 255)  # Blue
        print("Button 0 (Blue) pressed: Blue")

    elif not helper.button47.value():  # Button 47 pressed (Red)
        helper.rgb_led(255, 0, 0)  # Red
        print("Button 47 (Red) pressed: Red")

    elif not helper.button48.value():  # Button 48 pressed (Green)
        helper.rgb_led(0, 255, 0)  # Green
        print("Button 48 (Green) pressed: Green")

    else:
        helper.rgb_led(0, 0, 0)  # Turn off the LED if no buttons are pressed
        print("No button pressed: LED off")

    sleep(0.1)  # Debounce delay
