# ESP32 Tic-Tac-Toe Game with ESP-NOW Communication

This project is a Tic-Tac-Toe game that runs on two Lolin S3 Mini Pro devices and uses ESP-NOW for peer-to-peer communication. The game uses the onboard TFT display for showing the game board and physical buttons for user input.

## Features

- Two-player Tic-Tac-Toe game over ESP-NOW.
- Visual representation on the built-in TFT display.
- Built-in buttons for controlling the cursor and marking moves.
- RGB LED to indicate the current player.
- Displays the winner or draw status after game completion.

## Hardware Requirements

- 2x Lolin S3 Mini Pro boards (ESP32-based)

## Installation

### 1. Required Libraries

This project requires the following Python libraries to be installed on your Lolin S3 Mini Pro board:

- `espnow` for ESP-NOW communication
- `network` for WiFi configuration
- `machine` for pin control
- `st7789py` for TFT display control
- Custom modules such as `tft_config` for setting up the display, and `helper` for button and LED control.

### 2. Setup

1. Clone or copy the repository to your local system.
2. Upload the Python scripts (`main.py`, `tft_config.py`, `helper.py`, etc.) to your ESP32 using a tool such as [ampy](https://github.com/scientifichackers/ampy) or [Thonny](https://thonny.org/).
3. Update the MAC addresses of the peer devices in the `main.py` script.

To retrieve the MAC address of your Lolin S3 Mini Pro board, you can use the following Python snippet:


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