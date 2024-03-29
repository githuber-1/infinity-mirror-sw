import network

class EspNetwork():
    """
    TODO: Add SSID and PW. Store them in flash memory.
    TODO: Implement disconnect
    """
    SSID = ""
    PW = ""
    
    def __init__(self):
        self.timeout = 1 
        
    def connect(self) -> bool:
        self.station = network.WLAN(network.STA_IF)
        self.station.active(True)
        if not self.station.isconnected():
            print('Connecting to network...')
            self.station.connect(self.SSID, self.PW)
            while not self.station.isconnected():
                pass
        print(f'network config: {self.station.ifconfig()}')

    def disconnect(self) -> bool:
        pass


