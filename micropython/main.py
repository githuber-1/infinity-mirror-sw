from clock import Clock
from peripherals import Peripherals
from ledController import LEDController
from enum import Enum

class Mode(Enum):
    pass

class infinityMirror():
    """
    Application level class for managing infinity mirror clock, LEDs, and Peripherals
    """
    def __init__(self):
        self.clock = Clock()
        self.leds = LEDController()
        self.peripherals = Peripherals()

    def displayTime(self) -> None:
        # TODO Update to utilize palette
        now = self.clock.getTime()
        self.leds.ledClock(now)


def main():
    # Initialization on boot up
    infinity = infinityMirror()
    # init RTC time using SNTP
    infinity.clock.setRTCStartTime()

    # Loop
    while True:
        # Mode handled by interrupts
        pass


if __name__ == "__main__":
    main()