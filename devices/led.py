from logger import get_logger
from machine import Pin, Timer
from utime import sleep,ticks_ms
from devices.device import Device

logger=get_logger()

class Led(Device):
    def __init__(self, dev_ht,name, pin,config):
        logger.debug(f"Create Led <{name}> Pin <{pin}>")
        super().__init__(dev_ht,name, pin,config)
            
        self.initial_state=config.get("initial_state",1)
        self.value=self.initial_state
        self.pin=Pin(pin,Pin.OUT)
        self.pin.value(self.initial_state)
        self.mode=config.get("mode","solid")
        self.blink_speed=config.get("blink_speed",1000)
        self.blink_off_speed=config.get("blink_off_speed",self.blink_speed)
        self.initial_delay=config.get("initial_delay",0)
        self.nextupdate=ticks_ms()+self.blink_speed+self.initial_delay
        self.auto_off_time=config.get("auto_off_time",0)
        self.last_on_ask=ticks_ms()
        self.actions=self.config.get("actions",[])
        
    
    def run(self):
        if self.mode=="blink":
            if ticks_ms()>self.nextupdate:
                logger.debug(f"Must blink {self.name}")
                if self.value==0:
                    self.value=1
                else:
                    self.value=0
                if not self.suspended:
                    self.pin.value(self.value)
                if self.value==0:
                    self.nextupdate=self.nextupdate+self.blink_off_speed
                else:
                    self.nextupdate=self.nextupdate+self.blink_speed
        if self.auto_off_time and self.last_on_ask+self.auto_off_time<ticks_ms() and self.pin.value()==1:
            logger.info(f"Auto off {self.name}")
            self.pin.value(0)
            self.value=0
            self.callback(self.pin)
            

    
    def toggle(self):
        self.pin.toggle()
    
    def set_value(self,value):
        self.value=value
        if value!=self.pin.value():
            self.callback(self.pin)
            
        if value==1:
            self.last_on_ask=ticks_ms()
        self.pin.value(value)