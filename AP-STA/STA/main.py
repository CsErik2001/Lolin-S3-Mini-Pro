import network
import socket
import time
import s3minipro as helper
from machine import Pin
import tft_config
import vga1_8x16 as font
import _thread

# Initialize pins and TFT display
rgb = Pin(helper.RGB_POWER, Pin.OUT)
button0 = helper.button0
button47 = helper.button47
button48 = helper.button48
tft = tft_config.config(0)  # Initialize the TFT display


def set_led_color(color):
    if color == 'green':
        rgb.value(1)  # Turn on RGB LED power
        helper.rgb_led(0, 1, 0)  # Green
    elif color == 'red':
        rgb.value(1)  # Turn on RGB LED power
        helper.rgb_led(1, 0, 0)  # Red
    else:
        rgb.value(0)  # Turn off RGB LED


# Connect to Access Point
sta = network.WLAN(network.STA_IF)
sta.active(True)
sta.connect('ESP32-AP', '123456789')

# Wait for connection
while not sta.isconnected():
    time.sleep(1)

print('Connected with IP:', sta.ifconfig()[0])

set_led_color('green')  # Set LED to green when connected

# Connect to AP and set up the socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('192.168.4.1', 8080))  # Replace with the actual AP's IP address


def receive_data():
    while True:
        try:
            data = s.recv(1024)
            if data:
                message = data.decode('utf-8')
                print('Received from AP:', message)
                tft.text(font, message, 0, 0)
        except Exception as e:
            print('Error:', e)
            set_led_color('red')  # Set LED to red if there is an error
            break


def send_data():
    while True:
        try:
            # Determine which button is pressed and send the message
            if button0.value() == 0:
                message = 'Button 0 Pressed'
            elif button47.value() == 0:
                message = 'Button 47 Pressed'
            elif button48.value() == 0:
                message = 'Button 48 Pressed'
            else:
                message = 'No Button Pressed'

            # Send the message
            data_to_send = message.encode('utf-8')
            s.send(data_to_send)
            time.sleep(1)  # Adjust the frequency as needed
        except Exception as e:
            print('Error:', e)
            set_led_color('red')  # Set LED to red if there is an error
            break


# Start threads for sending and receiving data
_thread.start_new_thread(receive_data, ())
_thread.start_new_thread(send_data, ())
