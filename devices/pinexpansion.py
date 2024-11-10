from drivers.pcf8574 import PCF8574

from logger import get_logger
from machine import Pin, Timer, I2C
from utime import sleep,ticks_ms
from devices.device import Device
import utime

logger=get_logger()

class PinExpander(Device):
    def __init__(self, dev_ht, name, pin,config):
        logger.info(f"Create Pin Expander <{name}> Pin <{pin}>")
        super().__init__(dev_ht,name, pin,config)
        self.sda=Pin(pin)
        self.i2c = I2C(0, sda=self.sda, scl=Pin(pin+1), freq=400000)
        self.pcf = PCF8574(self.i2c, self.config.get("i2c_addr",0x20))
        self.poll_speed=1000
        self.nextupdate=ticks_ms()+self.poll_speed
        self.count=0
        self.initialized=False        
        try:
            self.pcf.check()
            self.initialized=True
        except Exception as e:
            logger.error(f"Unable to init expansion {self}")

        
    
