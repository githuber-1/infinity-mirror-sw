import time, utime, ntptime
from peripherals import Peripherals
from espnetwork import EspNetwork
from ledController import LedController

class Tester():
    def __init__(self):
        self.espNetwork = EspNetwork()
        self.encoderTester = Peripherals(34, 35, 25)
        self.ledController = LedController(33)
        self.timezone = -6
        self.time = None

    def convert_time(self):
        newTime = utime.localtime(utime.mktime(utime.localtime()) + self.timezone * 3600)
        self.time = [newTime[3], newTime[4], newTime[5]]
    
    def test_wifi(self):
        print('\n---Testing WiFi Connection---')
        self.espNetwork.connect()
        if self.espNetwork.station.isconnected():
            print(f'	WiFi test passed')
            return True
        print(f'	WiFi test failed')
        return False

    def test_clock(self):
        print('\n---Testing SNTP / Clock---')
        currentTime = utime.localtime()
        ntptime.settime()
        self.convert_time()

        print(f'Current time is {self.time[0]}:{self.time[1]}:{self.time[2]}')
        resp = input('If time is correct, enter "y", if not, enter "n": ')
        if resp == "y":
            print(f'	SNTP / Clock test passed')
            return True
        print(f'	SNTP / Clock test failed')
        return False

    def test_button(self):
        print('\n---Testing Encoder Button---')
        currentVal = self.encoderTester.btnVal
        resp = input('Enter "y" while pressing button to continue, "n" to cancel test, and "s" to skip: ')
        if resp == 'y':
            if currentVal != self.encoderTester.btnVal:
                print(f'	Button test passed, initial value: {currentVal}, new value: {self.encoderTester.btnVal}')
                return True
        print(f'	Button test failed, initial value: {currentVal}, new value: {self.encoderTester.btnVal}')
        return False

    def test_encoder(self):
        print('\n---Testing Encoder---')
        currentVal = self.encoderTester.rotaryEncoder.value()
        resp = input(f'Prepare to turn encoder. Enter "y" to proceed, "n" to cancel test, and "s" to skip: ')
        print('You have 10 seconds to turn the encoder.')
        if resp == 'y':
            startTime = time.time()
            while time.time() - startTime < 10:
                if currentVal != self.encoderTester.rotaryEncoder.value():
                    print(f'	Encoder test passed, initial value: {currentVal}, newVal: {self.encoderTester.rotaryEncoder.value()}')
                    return True
        print(f'	Encoder test failed, initial value: {currentVal}, new value: {self.encoderTester.rotaryEncoder.value()}')
        return False

    def test_leds(self):
        print(f'\n---Testing LEDs---')
        print('Running cycle for 20s')
        startTime = utime.time()
        while utime.time() - startTime < 20:
            self.convert_time()
            self.ledController.ledClock(self.time)
            utime.sleep(0.25)
        self.ledController.killLeds()
        resp = input(f'Did LED Clock function as expected? Enter "y" or "n": ')
        if resp == "y":
            print(f'	LED Test Passed')
            return True
        print(f'LED Test Failed')
        return False

    def checkout(self):
        self.test_wifi()
        self.test_clock()
        self.test_button()
        self.test_encoder()
        self.test_leds()

if __name__ == "__main__":
    tester = Tester()
    tester.checkout()
