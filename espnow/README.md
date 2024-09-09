# ESP-NOW Project Demo

## Introduction:

This project demonstrates the use of the ESP-NOW protocol for communication between two Lolin S3 Mini Pro modules. Although the code can run on any ESP32/ESP8266 module, the hardware setup is specifically designed for the Lolin S3 Mini Pro.

The same code can be deployed on both devices. The only required change is to set the correct MAC address for each module. Below is a Python snippet to retrieve the MAC address:

## Code to get MAC address:
```python
import network

def get_mac_address():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    mac = wlan.config('mac')
    return b''.join([bytes([b]) for b in mac])

# Get MAC address in the required format
mac_address = get_mac_address()
print("MAC address in byte format:", mac_address)
```

*Please note that MAC address should be in bits.*

## Usage of the code:
There are three buttons on the Lolin S3 Mini Pro board. When you press a button, the corresponding action will be displayed on the other board.






