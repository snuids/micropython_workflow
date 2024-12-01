from logger import get_logger
from machine import Pin, Timer, I2C
from utime import sleep,ticks_ms
from devices.device import Device

import ustruct
import math

logger=get_logger()


class TimeOfFlight(Device):
    def __init__(self, dev_ht, name, pin,config):
        logger.debug(f"Create TOF <{name}> Pin <{pin}>")
        super().__init__(dev_ht,name, pin,config)
        self.actions=self.config.get("actions",[])
        self.sda=Pin(pin)
        self.i2c = I2C(0, sda=self.sda, scl=Pin(pin+1), freq=400000)
        self.poll_speed=500
        self.nextupdate=ticks_ms()+self.poll_speed
        
        self.value=0
        self.data = bytearray(2)
        
    def run(self):
        if ticks_ms()<self.nextupdate:
           return
        try:
            self.nextupdate=ticks_ms()+self.poll_speed
            self.i2c.readfrom_mem_into(0x52, 0, self.data)
            distance = self.data[0] << 8 | self.data[1]
            logger.debug(f"Distance {distance}")
            self.value=distance
            
            self.callback(self.sda)
        except Exception as e:
            logger.error("Unable to compute tof")
            logger.error(e)
