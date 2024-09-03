import network
import socket
import s3minipro as helper
from machine import Pin
import time
import _thread
import tft_config
import vga1_8x16 as font

rgb = Pin(helper.RGB_POWER, Pin.OUT)

# Initialize the RGB LED and buttons
button0 = helper.button0
button47 = helper.button47
button48 = helper.button48

# Initialize the TFT display
tft = tft_config.config(0)

# Set up Access Point with a password
ap = network.WLAN(network.AP_IF)
ap.active(True)
ap.config(essid='ESP32-AP', password='123456789', authmode=network.AUTH_WPA_WPA2_PSK)

print('AP active with IP:', ap.ifconfig()[0])


# Set LED to red initially

# Set up a socket to listen for connections
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 8080))
s.listen(1)

def handle_client(conn):
    while True:
        try:
            # Check button states and send corresponding messages
            if button0.value() == 0:
                message = 'Button 0 Pressed'
            elif button47.value() == 0:
                message = 'Button 47 Pressed'
            elif button48.value() == 0:
                message = 'Button 48 Pressed'
            else:
                message = 'No Button Pressed'

            # Encode and send the message
            data_to_send = message.encode('utf-8')
            conn.send(data_to_send)

            # Receive data from client
            data_received = conn.recv(1024)
            text = data_received.decode('utf-8')
            if data_received:
                tft.text(font, text, 0, 0)
                if text == 'Button 0 Pressed':
                    rgb.value(1)
                    helper.rgb_led(0, 0, 1)
                elif text == 'Button 47 Pressed':
                    rgb.value(1)
                    helper.rgb_led(1, 0, 0)
                elif text == 'Button 48 Pressed':
                    rgb.value(1)
                    helper.rgb_led(0, 1, 0)
                else:
                    rgb.value(0)

            # Add a short delay to prevent excessive updates
            time.sleep(0.1)
        except Exception as e:
            print('Error:', e)
            break
    conn.close()

# Start a thread to monitor client connections

while True:
    try:
        conn, addr = s.accept()
        _thread.start_new_thread(handle_client, (conn,))
    except Exception as e:
        pass
