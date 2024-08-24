import network
import time
import s3minipro as helper
from machine import Pin
import tft_config
import vga1_8x16 as font
import urequests as requests

# Wi-Fi credentials and API settings
SSID = ""
PASSWORD = ""
CITY = ""
API_KEY = ""
UPDATE_INTERVAL = 120

# Initialize components
def init_wifi(ssid, password):
    station = network.WLAN(network.STA_IF)
    station.active(True)
    station.config(hostname="S3MiniPro")
    station.connect(ssid, password)
    return station

def wait_for_connection(station):
    while not station.isconnected():
        display_status("Connecting to network...")
        helper.rgb_led(0, 1, 0)  # Green LED
        time.sleep(1)
    print("Network config:", station.ifconfig()[0])

def init_display():
    rgb = Pin(helper.RGB_POWER, Pin.OUT)
    rgb.value(1)  # Enable RGB power
    return tft_config.config(0)

# Fetch weather data
def get_weather_data(city, api_key):
    api = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric&lang=en'
    response = requests.get(api)
    return response.json() if response.status_code == 200 else None

# Display functions
def display_status(message):
    display.fill(0)  # Clear display
    display.text(font, message, 0, 0)

def display_weather(weather_data):
    display.fill(0)  # Clear display
    display_weather_icon(weather_data['weather'][0]['icon'])
    display.text(font, f"Temp: {round(weather_data['main']['temp'], 1)}C", 0, 80)
    display.text(font, f"Hum: {weather_data['main']['humidity']}%", 0, 100)

def display_weather_icon(icon_code):
    try:
        icon_module = __import__(f'icons._{icon_code}', globals(), locals(), ['icon'], 0)
        display.bitmap(icon_module, 14, -10, 0)
    except ImportError:
        print("Icon not found!")

# Initialize buttons and views
views = ["Weather", "Settings", "About"]
current_view = 0


# View navigation functions
def update_view():
    global current_view
    if views[current_view] == "Weather":
        weather_data = get_weather_data(CITY, API_KEY)
        if weather_data:
            display_weather(weather_data)
        else:
            display_status("Failed to get weather data")
    elif views[current_view] == "Settings":
        display_status("Settings View")
    elif views[current_view] == "About":
        display_status("About View")

def switch_to_previous_view(pin):
    global current_view
    current_view = (current_view - 1) % len(views)
    update_view()

def switch_to_next_view(pin):
    global current_view
    current_view = (current_view + 1) % len(views)
    update_view()

# Attach interrupts to buttons
helper.button0.irq(trigger=Pin.IRQ_FALLING, handler=switch_to_previous_view)
helper.button48.irq(trigger=Pin.IRQ_FALLING, handler=switch_to_next_view)
helper.button47.irq(trigger=Pin.IRQ_FALLING, handler=lambda pin: display_status("Action!"))

# Main loop
def main():
    station = init_wifi(SSID, PASSWORD)
    wait_for_connection(station)
    helper.rgb_led(0, 1, 0)  # Red LED

    while True:
        if views[current_view] == "Weather":
            update_view()
        time.sleep(UPDATE_INTERVAL)

# Initialize display and start the main loop
display = init_display()
update_view()  # Show the initial view
main()