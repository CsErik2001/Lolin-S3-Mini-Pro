import network
import espnow
import vga1_8x16 as font
import tft_config
import time
import s3minipro as helper

tft = tft_config.config()
b1 = helper.button0
b2 = helper.button47
b3 = helper.button48

# A WLAN interface must be active to send()/recv()
sta = network.WLAN(network.STA_IF)
sta.active(True)
sta.disconnect()   # Ensure it doesn't auto-connect to AP

e = espnow.ESPNow()
e.active(True)

# MAC addresses of the peers
peer = b''  # Replace with the MAC address of the other device
e.add_peer(peer)

def send_message(msg, e):
    try:
        e.send(peer, msg.encode())  # Encode string to bytes
        print("Message sent:", msg)
    except Exception as e:
        print("Send error:", e)

def receive_message(e):
    try:
        host, msg = e.recv(500)  # Add a timeout of 500 ms (0.5 seconds)
        if msg:
            tft.fill(0x0000)
            decoded_msg = msg.decode()  # Decode bytes to string
            print("Message received:", decoded_msg)
            return decoded_msg
        else:
            return None
    except Exception as e:
        print("Receive error:", e)
        return None

while True:
    print("Looping...")
    print(f"Button 1 value: {b1.value()}")

    if b1.value() == 0:
        print("Button 1 pressed")
        send_message("Btn 1 pressed", e)  # Send a message when button is pressed
    elif b2.value() == 0:
        print("Button 2 pressed")
        send_message("Btn 2 pressed", e)
    elif b3.value() == 0:
        print("Button 3 pressed")
        send_message("Btn 3 pressed", e)

    # Receive a message
    msg = receive_message(e)
    print(f"Received message: {msg}")

    if msg:
        tft.text(font, msg, 0, 0)  # Display the decoded string
        print("Received:", msg)
        if msg == "end":  # Compare with the string "end"
            break
    else:
        tft.text(font, "Waiting...", 0, 16)
        print("Waiting...")

    time.sleep(1)  # Adjust delay as needed

# Clean up
e.deinit()
