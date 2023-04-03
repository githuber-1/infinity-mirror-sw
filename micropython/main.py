from clock import Clock
from peripherals import Peripherals
from ledController import LEDController
from espnetwork import ESPNetwork
import date

# TODO implement secondary function for encoder based on button press

class infinityMirror():
    """
    Application level class for managing infinity mirror clock, LEDs, and Peripherals
    """
    MODE_CLOCK = 0
    MODE_STATIC = 1
    MODE_RAINBOW = 2
    MODE_COLORWAVE = 3
    MODE_KALEIDOSCOPE = 4

    def __init__(self):
        self.clock = Clock()
        self.leds = LEDController()
        self.peripherals = Peripherals()
        self.espnetwork = ESPNetwork()

    def clock(self) -> None:
        # TODO Update to utilize color palettes
        now = self.clock.getTime()
        self.leds.ledClock(now)

    def static(self) -> None:
        pass

    def rainbow(self) -> None:
        pass

    def colorwave(self) -> None:
        pass

    def kaleidoscope(self) -> None:
        pass


def main():
    # boot
    infinity = infinityMirror()
    # init RTC time using SNTP
    infinity.espnetwork.connect()
    infinity.clock.setRTCStartTime()
    infinity.espnetwork.disconnect()

    # main loop
    while True:
        # get mode from encoder value
        # disable ISR during read to avoid race condition
        enc_val = infinity.peripherals.rotaryEncoder.btnVal()
        
        if enc_val == infinity.MODE_CLOCK:
            infinity.clock()
        elif enc_val == infinity.MODE_STATIC:
            infinity.static()
        elif enc_val == infinity.MODE_RAINBOW:
            infinity.rainbow()
        elif enc_val == infinity.MODE_COLORWAVE:
            infinity.colorwave()
        elif enc_val == infinity.MODE_KALEIDOSCOPE:
            infinity.kaleidoscope()

        time.sleep(50)


if __name__ == "__main__":
    main()