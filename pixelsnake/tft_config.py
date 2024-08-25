from machine import Pin, SPI
import st7789py as st7789
import s3minipro as helper

def config(rotation=0):

    return st7789.ST7789(
        SPI(2, baudrate=40000000, sck=Pin(helper.SPI_CLK), mosi=Pin(helper.SPI_MOSI), miso=Pin(helper.SPI_MISO)),
        128,
        128,
        reset=Pin(helper.TFT_RST, Pin.OUT),
        cs=Pin(helper.TFT_CS, Pin.OUT),
        dc=Pin(helper.TFT_DC, Pin.OUT),
        backlight=Pin(helper.TFT_BL, Pin.OUT),
        rotation=rotation,
        color_order=st7789.BGR,
    )

