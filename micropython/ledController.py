from neopixel import NeoPixel
from machine import Pin

class LEDController:
    def __init__(self, led_pin: int, num_leds: int):
        self.num_leds = num_leds
        # Initalize led_pin
        Pin(13, Pin.Out)
        self.leds = NeoPixel(Pin(led_pin), self.num_leds)

def main():
    pass

if __name__ == '__main__':
    main()


