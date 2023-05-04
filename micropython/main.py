from peripherals import Peripherals
from ledController import LedController
from espnetwork import EspNetwork
import utime, ntptime

# TODO implement secondary function for encoder based on button press

class infinityMirror():
    """
    Application level class for managing infinity mirror clock, LEDs, and Peripherals
    """
    # mode constants
    NUM_MODES = 6
    MODE_CLOCK = 0
    MODE_FIRE = 1
    MODE_STATIC = 2
    MODE_COLORWAVE = 3
    MODE_RAINBOW = 4
    MODE_KALEIDOSCOPE = 5
    
    # timing constants
    NTP_ATTEMPTS = 3
    BLE_TIME_MS = 3000
    DEBOUNCE_TIME_MS = 20
    LOOP_DELAY_MS = (1 / 50) * 1000
    BLE_LOOP_DELAY_MS = 500

    def __init__(self):
        self.espNetwork = EspNetwork()
        self.leds = LedController(33)
        self.peripherals = Peripherals(34, 35, 25)
        #TODO timezone should not be hardcoded
        self.timezone = -6
        self.led_mode = 0
        self.ble = False
        
        # button handling
        self.btn_was = 1
        self.btn_dwn_time = None
    
        # get time
        self.espNetwork.connect()
        self.set_time()
        self.time = self.get_time()
        self.espNetwork.disconnect()

    def set_time(self):
        initial_time = utime.localtime()
        attempts_remaining = self.NTP_ATTEMPTS
        while attempts_remaining > 0:
            try:
                ntptime.settime()
            except Exception as e: 
                print(f'Exception: {e}, trying {attempts_remaining} more times')
            attempts_remaining -= 1

    def get_time(self):
        newTime = utime.localtime(utime.mktime(utime.localtime()) + self.timezone * 3600)
        self.time = [newTime[3], newTime[4], newTime[5]]
        
    def handle_button(self):
        btn_val = self.peripherals.btnPin.value()

        # button was just pressed
        if btn_val == 0 and self.btn_was == 1:
            self.btn_dwn_time = utime.ticks_ms()
            
        # button was released after debounce period
        elif btn_val == 1 and self.btn_was == 0 and utime.ticks_ms() - self.btn_dwn_time > self.DEBOUNCE_TIME_MS and utime.ticks_ms() - self.btn_dwn_time < self.BLE_TIME_MS:
            self.led_mode += 1
            print(f'get mode: {self.led_mode} ')
            if self.led_mode >= self.NUM_MODES:
                self.led_mode = 0
                
        # button was released after BLE period
        elif btn_val == 1 and self.btn_was == 0 and (utime.ticks_ms() - self.btn_dwn_time) > self.BLE_TIME_MS:
            self.ble = not self.ble
            self.leds.clear()
            print(f'BLE Mode: {self.ble}')
        
        self.btn_was = btn_val
                

def main():
    # boot
    infinity = infinityMirror()
    start_time = utime.ticks_ms()
    infinity.handle_button()
    enc_val = infinity.peripherals.rotaryEncoder.value()
    
    # init LED vars
    # colorwave
    start_led = 0
    hue = 0
    # 
    first_color = 0
    
    # main loop
    while True:

        if utime.ticks_ms() - start_time > infinity.LOOP_DELAY_MS:
            if not infinity.ble:

                if infinity.led_mode == infinity.MODE_CLOCK:
                    infinity.get_time()
                    infinity.leds.led_clock(infinity.time, enc_val)
                    
                elif infinity.led_mode == infinity.MODE_FIRE:
                    infinity.leds.fire(enc_val)
                    
                elif infinity.led_mode == infinity.MODE_STATIC:
                    infinity.leds.static(enc_val)
                    
                elif infinity.led_mode == infinity.MODE_COLORWAVE:
                    start_led, hue = infinity.leds.colorwave(enc_val, start_led, hue)
                        
                elif infinity.led_mode == infinity.MODE_RAINBOW:
                    start_led = infinity.leds.rainbow(enc_val, start_led)               

                elif infinity.led_mode == infinity.MODE_KALEIDOSCOPE:
                    first_color = infinity.leds.kaleidoscope(enc_val, first_color)

                # update time
                start_time = utime.ticks_ms()
                
            # in BLE config mode, used for partitioning
            else:
                if utime.ticks_ms() - start_time > infinity.BLE_LOOP_DELAY_MS:
                    infinity.leds.ble()
                    # update time
                    start_time = utime.ticks_ms()
                    
        infinity.handle_button()
        enc_val = infinity.peripherals.rotaryEncoder.value()


if __name__ == "__main__":
    main()
