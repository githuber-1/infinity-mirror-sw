from neopixel import NeoPixel
from machine import Pin
import random, math
# TODO Color Palette Control

class LedController:
    NUM_LEDS = 60
    ENC_TO_HSV_MAP = 1270
    MAX_HUE = 65536
    
    def __init__(self, led_pin: int):
        
        # Initalize led_pin
        Pin(led_pin, Pin.OUT)
        self.leds = NeoPixel(Pin(led_pin), self.NUM_LEDS)
        
        self.palette = None

    def rainbow(self):
        pass

    def set_palette(self, palette):
        self.palette = palette

    def led_clock(self, time, enc_val) -> None:
        hour = time[0]
        if hour > 12:
            hour = hour - 12
        hour = (hour * 5) - 31
        minute = time[1] - 31
        second = time[2] - 31
        start_color = enc_val * self.ENC_TO_HSV_MAP
        
        hour_color = self.colorHSV(start_color, 255, 255)
        min_sec_color = self.colorHSV(start_color, 150, 200)

        for i in range(self.NUM_LEDS):
            self.leds[i] = (0, 0, 0)
        
        self.leds[hour] = hour_color
        self.leds[hour - 1] = hour_color
        self.leds[hour + 1] = hour_color
        self.leds[minute] = min_sec_color
        self.leds[second] = min_sec_color
        self.leds.write()
    
    def fire(self, enc_val) -> None:
        start_color = enc_val * self.ENC_TO_HSV_MAP
        for i in range(self.NUM_LEDS):
            #color = self.colorHSV(5000, random.randrange(0, 255), random.randrange(0, 255))
            color = self.colorHSV(random.randrange(start_color, start_color + 2000), 255, random.randrange(0, 255))
            self.leds[i] = color
        self.leds.write()
    
    def static(self, enc_val) -> None:
        start_color = enc_val * self.ENC_TO_HSV_MAP
        color = self.colorHSV(start_color, 255, 255)
        self.leds.fill(color)
        self.leds.write()
        pass

    def colorwave(self, enc_val, start_led, hue):
        wave_leds = math.floor( enc_val * 0.4 ) + 1
        brightness_delta = math.floor( 255 / wave_leds )
        hue_delta = math.floor( self.MAX_HUE / 250 )
        self.clear()
        
        led_num = 0
        for i in range(start_led, start_led - wave_leds, -1):
            color = self.colorHSV(hue, 255, 255 - ( brightness_delta * led_num ) )
            self.leds[i] = color
            led_num += 1
        self.leds.write()
        
        start_led += 1
        if start_led > 59:
            start_led = 0
            
        hue += hue_delta
        if hue > self.MAX_HUE:
            hue = 0
            
        return start_led, hue

    def rainbow(self, enc_val, start_led):
        saturation = math.floor( 255 - (enc_val * 4) )
        led_num = 0
        for i in range(start_led, start_led - 59, -1):
            hue = math.floor( ( self.MAX_HUE / 60) * led_num )
            color = self.colorHSV(hue, saturation, 255)
            self.leds[i] = color
            led_num += 1
        self.leds.write()
        
        start_led += 1
        if start_led > 59:
            start_led = 0
        
        return start_led

    def kaleidoscope(self, enc_val, first_color):
        hue_delta = math.floor(self.MAX_HUE / 2)
        rate = math.floor(2570 / 2)
        num_patterns = int((enc_val / 5) + 2)
        first_color += rate
        if first_color > self.MAX_HUE:
            first_color = 0
        last_color = first_color + hue_delta
        if last_color > self.MAX_HUE:
            last_color = first_color + hue_delta - self.MAX_HUE
        
        print(enc_val, num_patterns)
        
        for i in range(0, num_patterns):

            if i % 2 == 0:
                for j in range(0, math.floor(self.NUM_LEDS / num_patterns)):
                    color = self.colorHSV(first_color - (2500 * j), 255, 255)
                    self.leds[(i * math.floor((self.NUM_LEDS / num_patterns))) + j] = color
            if i % 2 == 1:
                for j in range(0, math.floor(self.NUM_LEDS / num_patterns)):
                    color = self.colorHSV(last_color - (2500 * j), 255, 255)
                    self.leds[(i * math.floor((self.NUM_LEDS / num_patterns))) + j] = color

        self.leds.write()
        
        return first_color
        
    
    def ble(self) -> None:
        current_state = self.leds[-1]
        if current_state[2] > 0:
            for i in range(self.NUM_LEDS):
                self.leds[i] = (0, 0, 0)
        else:
            self.leds[-1] = (0, 0, 255)
            self.leds[14] = (0, 0, 255)
            self.leds[29] = (0, 0, 255)
            self.leds[44] = (0, 0, 255)
        self.leds.write()

    def clear(self):
        self.leds.fill((0, 0, 0))
        self.leds.write()

    def hue():
        pass

    def colorHSV(self, hue, sat, val):
        """
        Converts HSV color to rgb tuple and returns it.
        The logic is almost the same as in Adafruit NeoPixel library:
        https://github.com/adafruit/Adafruit_NeoPixel so all the credits for that
        go directly to them (license: https://github.com/adafruit/Adafruit_NeoPixel/blob/master/COPYING)
        :param hue: Hue component. Should be on interval 0-65535
        :param sat: Saturation component. Should be on interval 0-255
        :param val: Value component. Should be on interval 0-255
        :return: (r, g, b) tuple
        """
        if hue >= self.MAX_HUE:
            hue %= self.MAX_HUE

        hue = (hue * 1530 + 32768) // self.MAX_HUE
        if hue < 510:
            b = 0
            if hue < 255:
                r = 255
                g = hue
            else:
                r = 510 - hue
                g = 255
        elif hue < 1020:
            r = 0
            if hue < 765:
                g = 255
                b = hue - 510
            else:
                g = 1020 - hue
                b = 255
        elif hue < 1530:
            g = 0
            if hue < 1275:
                r = hue - 1020
                b = 255
            else:
                r = 255
                b = 1530 - hue
        else:
            r = 255
            g = 0
            b = 0

        v1 = 1 + val
        s1 = 1 + sat
        s2 = 255 - sat

        r = ((((r * s1) >> 8) + s2) * v1) >> 8
        g = ((((g * s1) >> 8) + s2) * v1) >> 8
        b = ((((b * s1) >> 8) + s2) * v1) >> 8

        return r, g, b


def main():
    pass

if __name__ == '__main__':
    main()
