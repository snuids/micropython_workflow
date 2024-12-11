from logger import get_logger
from machine import Pin, Timer
from utime import sleep,ticks_ms
from devices.device import Device
from devices.led import Led

logger=get_logger()


class Battery(Device):
    def __init__(self, dev_ht, name, pin,config):
        logger.debug(f"Create Battery <{name}> Pin <{pin}>")
        super().__init__(dev_ht,name, pin,config)
        self.nextupdate=ticks_ms()+100
        self.last_change=ticks_ms()

        
        self.leds=[]
        
        for i in range(0,3):
            led=Led(dev_ht,f"name_{i+1}",pin+i,{})
            self.leds.append(led)
            dev_ht[led.name]=led
            
    def set_value(self,value):
        self.last_change=ticks_ms()
#        value=3.15
        self.value=value
        if value>3.2:
            self.leds[0].set_on()
            self.leds[1].set_on()
            self.leds[2].set_on()
        elif value>3.1:
            self.leds[0].set_blink()
            self.leds[1].set_on()
            self.leds[2].set_on()
        elif value>3.0:
            self.leds[0].set_off()
            self.leds[1].set_on()
            self.leds[2].set_on()
        elif value>2.9:
            self.leds[0].set_off()
            self.leds[1].set_blink()
            self.leds[2].set_on()                                                
        elif value>2.8:
            self.leds[0].set_off()
            self.leds[1].set_off()
            self.leds[2].set_on()
        else:
            A/0
            self.leds[0].set_off()
            self.leds[1].set_off()
            self.leds[2].set_blink()
            
    def blink(self):
        self.last_change=ticks_ms()+3000
        for i in range(0,3):
            self.leds[i].set_blink()
            
    def run(self):
        if self.last_change+5000<ticks_ms() and self.leds[0].value==1:
            for i in range(0,3):
                logger.debug("Reset Battery")
                self.leds[i].set_off()
                
            
        
            
    
    
            
