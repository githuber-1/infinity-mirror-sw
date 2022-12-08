from clock import Clock
from peripherals import Peripherals
from ledController import LEDController
from enum import Enum

class Mode(Enum):
    pass

class System():
    def __init__():
        self.clock = Clock()
        self.leds = LEDController()
        self.peripherals = Peripherals()

    def displayTime(self) -> None:
        now = self.clock.getTime()
        hour = now[0]
        minute = now[1]
        second = now[2]
        
        for i in range(self.num_leds):
            self.leds[i] = (0, 0, 0)
        
        self.leds[hour] = (255, 255, 255)
        self.leds[hour-1] = (255, 255, 255)
        self.leds[hour+1] = (255, 255, 255)
        self.leds[minute] = (255, 0, 0)
        self.leds[second] = (0, 255, 255)
        self.leds.write()

    def getMode(self):
        """
        Get rotary encoder value, map that to mode
        """
        self.peripherals.readEncoder()
        self.peripherals.readButton()


def main():
    # Initialization on boot up
    sys = System()
    # init RTC time
    sys.clock.setRTCStartTime()

    # Loop
    while True:
        sys.getMode()
        




if __name__ == "__main__":
    main()