from logger import get_logger
from machine import ADC, Timer
from utime import sleep,ticks_ms
from devices.device import Device

logger=get_logger()

class VoltageReader(Device):
    def __init__(self, dev_ht, name, pin,config):
        logger.debug(f"Create Voltage Reader <{name}> Pin <{pin}>")
        super().__init__(dev_ht,name, pin,config)
        self.pin=ADC(pin)
        self.nextupdate=ticks_ms()+100
        self.value=0
        self.data = bytearray(2)
        
    def run(self):
        if ticks_ms()<self.nextupdate:
           return
        try:
            self.nextupdate=ticks_ms()+self.poll_speed
            self.value=self.pin.read_u16()* 3.3 / 65536   
            logger.debug(f"ADC {self.value}")
            
            self.callback(self.pin)
        except Exception as e:
            logger.error("Unable to compute adc")
            logger.error(e)
        



