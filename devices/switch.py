from logger import get_logger
from machine import Pin, Timer
from utime import sleep,ticks_ms
from devices.device import Device

logger=get_logger()

class Switch(Device):
    def __init__(self, dev_ht, name, pin,config):
        logger.debug(f"Create Switch <{name}> Pin <{pin}>")
        super().__init__(dev_ht,name, pin,config)
        self.pin=Pin(pin, Pin.IN, pull=Pin.PULL_UP)
#        self.pin=Pin(pin, Pin.IN, pull=Pin.PULL_DOWN)        
#        self.pin.irq(trigger=Pin.IRQ_FALLING | Pin.IRQ_RISING, handler=self.callback)
        self.pin.irq(trigger=Pin.IRQ_FALLING, handler=self.callback)
        self.actions=self.config.get("actions",[])
        self.nextupdate=ticks_ms()+100
        

