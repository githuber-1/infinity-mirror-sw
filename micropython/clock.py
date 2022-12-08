import socket
import datetime
import struct
import pytz
import time
import utime
#from machine import RTC
#from ledController import ledController


class Clock():
    """
    Class that controls clock functions of ESP32  
    """
    NTP_SERVER = '0.uk.pool.ntp.org'
    NTP_DELTA = 2208988800
    #LEDS = ledController(13, 60)

    def __init__(self) -> None:
        self._tz = pytz.timezone('America/Denver')
        #self._rtc = RTC()
    
    def setRTCStartTime(self) -> None:
        """
        Use NTP to initialize the RTC.
        (TODO) Uncomment self._rtc line when ready to test on hardware
        """
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as client:
            data = '\x1b' + 47 * '\0'
            client.sendto(data.encode('utf-8'), (self.NTP_SERVER, 123))
            data, _ = client.recvfrom(256)
            tx_s, tx_f = struct.unpack('!12I', data)[10:12] # seconds and fractional seconds
            tx_timestamp = (tx_s + float(tx_f)/2**32) - self.NTP_DELTA

            now = datetime.datetime.fromtimestamp(tx_timestamp, self._tz)
            startTime = (now.year, now.month, now.day, now.hour, now.minute, now.second, now.microsecond)
            #self._rtc.datetime(startTime)
            print(f'time at boot is: {startTime}')

    def getTime(self) -> datetime:
        """
        Gets time from the RTC.
        Returns: datetime
        """
        time = []
        (year, month, mday, hour, minute, second, weekday, yearday) = utime.localtime()
        if hour > 12:
            hour = hour - 12
        print('current time is {}:{}:{}'.format(hour, minute, second))
        time = [hour, minute, second]
        
        return(time)


def main():
    while True:
        clock = Clock()
        clock.setRTCStartTime()
        clock.getTime()
        time.sleep(0.25)

if __name__ == "__main__":
    main()

