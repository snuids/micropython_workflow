from logger import get_logger
from machine import Pin, Timer, I2C
from utime import sleep,ticks_ms
from devices.device import Device

import ustruct
import math

logger=get_logger()

# Constants
ADXL345_ADDRESS = 0x53
ADXL345_POWER_CTL = 0x2D
ADXL345_DATA_FORMAT = 0x31
ADXL345_DATAX0 = 0x32

class Accelerometer(Device):
    def __init__(self, dev_ht, name, pin,config):
        logger.debug(f"Create Accelerometer <{name}> Pin <{pin}>")
        super().__init__(dev_ht,name, pin,config)
        self.actions=self.config.get("actions",[])
        self.sda=Pin(pin)
        self.i2c = I2C(0, sda=self.sda, scl=Pin(pin+1), freq=400000)
        self.i2c.writeto_mem(ADXL345_ADDRESS, ADXL345_POWER_CTL, bytearray([0x08]))  # Set bit 3 to 1 to enable measurement mode
        self.i2c.writeto_mem(ADXL345_ADDRESS, ADXL345_DATA_FORMAT, bytearray([0x0B]))  # Set data format to full resolution, +/- 16g
        self.poll_speed=500
        self.nextupdate=ticks_ms()+self.poll_speed
        
        self.pitch=0
        self.roll=0
        self.magnitude=0
        self.parameters=["pitch","roll","magnitude"]

    def run(self):
        if ticks_ms()<self.nextupdate:
           return
        try:
            self.nextupdate=ticks_ms()+self.poll_speed
            data = self.i2c.readfrom_mem(ADXL345_ADDRESS, ADXL345_DATAX0, 6)
            x, y, z = ustruct.unpack('<3h', data)
            self.magnitude=math.sqrt(x**2 + y**2 + z**2)
            self.roll=math.atan2(y, math.sqrt(x**2 + z**2)) * (180 / math.pi)
            self.pitch=math.atan2(-x, math.sqrt(y**2 + z**2)) * (180 / math.pi)
            

            logger.debug("X: {}, Y: {}, Z: {}, Magnitude: {:.2f}, Roll: {:.2f}, Pitch: {:.2f}".format(x, y, z, self.magnitude, self.roll, self.pitch))
            
            self.callback(self.sda)
        except Exception as e:
            logger.error("Unable to compute acceleration")
            logger.error(e)