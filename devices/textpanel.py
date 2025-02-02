from logger import get_logger
from machine import Pin, Timer, I2C,SoftI2C
from utime import sleep,ticks_ms
from devices.device import Device
from drivers.machine_i2c_lcd import I2cLcd
import gc

logger=get_logger()


class TextPanel(Device):
    def __init__(self, dev_ht, name, pin,config):
        logger.info(f"Create TextPanel <{name}> Pin <{pin}>")
        super().__init__(dev_ht,name, pin,config)
        self.nextupdate=ticks_ms()+100
        self.sda=Pin(pin)
        self.i2c = SoftI2C(sda=self.sda, scl=Pin(pin+1), freq=400000)
        self.initialized=False
        try:
            self.lcd = I2cLcd(self.i2c, self.config.get("i2c_addr",0x27)
                                      , self.config.get("i2c_num_rows",2)
                                      , self.config.get("i2c_num_cols",16))
            
            self.poll_speed=1000
            self.nextupdate=ticks_ms()+self.poll_speed
            self.lcd.putstr("SHINGAYKI")
            self.initialized=True
        except Exception as e:
            logger.error(f"Unable to start LCD {e}")

    def run(self):
        if  not self.initialized:
            return
        if ticks_ms()<self.nextupdate:
           return
        try:
            self.nextupdate=ticks_ms()+self.poll_speed
            if self.lcd.backlight:
#                self.lcd.backlight_off()
                pass
#            else:
#                self.lcd.backlight_on()
            self.lcd.clear()
            
            F = gc.mem_free()
            A = gc.mem_alloc()
            T = F+A
            P='{0:.2f}%'.format(F/T*100)
            mem= ('Total:{0} Free:{1} ({2})\r\n0123456789'.format(T,F,P))
            self.lcd.putstr(P)                
        except Exception as e:
            logger.error("Unable to set lcd")
            logger.error(e)
