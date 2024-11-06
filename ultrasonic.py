from logger import get_logger
from machine import Pin, Timer
from utime import sleep,ticks_ms,sleep_us,ticks_us
from devices.device import Device

logger=get_logger()

class UltraSonic(Device):
    def __init__(self, dev_ht, name, pin,config):
        logger.debug(f"Create Ultra Sonic <{name}> Pin <{pin}>")
        super().__init__(dev_ht,name, pin,config)
        self.trigger = Pin(pin, Pin.OUT)
        self.echo = Pin(config.get("echo_pin",pin+1), Pin.IN)
        self.actions=self.config.get("actions",[])
        self.poll_speed=500
        self.nextupdate=ticks_ms()+self.poll_speed
        self.value=0
        
    def run(self):
        if ticks_ms()<self.nextupdate:
           return
        try:
            self.nextupdate=ticks_ms()+self.poll_speed
            self.trigger.low()
            sleep_us(2)
            self.trigger.high()
            sleep_us(5)
            self.trigger.low()
            start=ticks_us()
            while self.echo.value() == 0:
               signaloff = ticks_us()
               if signaloff>start+100000:
                   raise ValueError("Trigger")
            while self.echo.value() == 1:
               signalon = ticks_us()
               if signaloff>start+100000:
                   raise ValueError("Echo")
               
            timepassed = signalon - signaloff
            distance = (timepassed * 0.0343) / 2
            self.value=int(distance)
            logger.debug(f"Distance {distance} cm")
            self.callback(self.trigger)
        except Exception as e:
            logger.error("Unable to compute distance")
            logger.error(e)

        


