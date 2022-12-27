from machine import Pin
import micropython
import sys
from rotary_irq_esp import RotaryIRQ
micropython.alloc_emergency_exception_buf(100)
# ISR info from https://docs.micropython.org/en/latest/reference/isr_rules.html
# # https://docs.micropython.org/en/latest/esp8266/tutorial/pins.html#
# https://github.com/miketeachman/micropython-rotary
# https://github.com/miketeachman/micropython-rotary/blob/master/Examples/example_simple.py
# https://github.com/miketeachman/micropython-rotary/blob/master/Examples/example_asyncio_class.py
# https://docs.micropython.org/en/latest/esp8266/tutorial/pins.html
# https://docs.openmv.io/library/mutex.html


class Peripherals():
    """
    TODO: Incorporate Mutexes as need to protect R/W of Encoder data
    TODO: Test rotaryEncoder module, make async (look at link above)
    Class for handling rotary encoder and button
    rotary encoder implements interrupts on both clk and dt pins
    """
    def __init__(self, enc_a_pin, enc_b_pin, btn_pin):
        rotaryEncoder = RotaryIRQ(pin_num_clk=enc_a_pin,
                                  pin_num_dt=enc_b_pin,
                                  min_val=0,
                                  max_val=5,
                                  reverse=False,
                                  range_mode=RotaryIRQ.RANGE_WRAP)
        
        btnPin = Pin(btn_pin, Pin.IN)
        btnVal = False

        print(f'Peripherals instantiated with {enc_a_pin, enc_b_pin, btn_pin}')

        # Button interrupt
        btnPin.irq(trigger=Pin.IRQ_FALLING, handler=self.btnCallback)

    def btnCallback(self, p):
        """
        Updates btnVal based on input pin value
        """
        self.btnVal = bool(p.value())
        print(f'btn: {self.btnVal}')
