from neopixel import NeoPixel
from machine import Pin
import datetime

# TODO Color Palette Control

class LEDController:
    NUM_LEDS = 60
    def __init__(self, led_pin: int):
        
        # Initalize led_pin
        Pin(13, Pin.Out)
        self.leds = NeoPixel(Pin(led_pin), self.NUM_LEDS)
        
        self.palette = None

    def rainbow(self):
        pass

    def setPalette(self, palette):
        self.palette = palette

    def ledClock(self, time: datetime) -> None:
        hour = time[0]
        minute = time[1]
        second = time[2]
        
        for i in range(self.NUM_LEDS):
            self.leds[i] = (0, 0, 0)
        
        self.leds[hour] = (255, 255, 255)
        self.leds[hour-1] = (255, 255, 255)
        self.leds[hour+1] = (255, 255, 255)
        self.leds[minute] = (255, 0, 0)
        self.leds[second] = (0, 255, 255)
        self.leds.write()

    def hue

def main():
    pass

if __name__ == '__main__':
    main()


