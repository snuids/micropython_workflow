from logger import get_logger
from utime import sleep,ticks_ms

logger=get_logger()

class Device():
    def __init__(self, dev_ht,name, pin,config):
        logger.debug(f"Create Device <{name}> Pin <{pin}>")
        self.pin_number=pin
        self.name = name
        self.config=config
        self.dev_ht=dev_ht
        self.debounce_delay=100
        self.next_callback=ticks_ms()+self.debounce_delay
        self.suspended=False
        
    def run(self):
        pass

    def callback(self,pin):

        if ticks_ms()>self.next_callback:
            
            self.next_callback=ticks_ms()+self.debounce_delay
            for action in self.actions:
                logger.debug(f"Execute {action}")
                if "condition" in action:
                    cond=eval(action["condition"].replace("value",str(self.value)))
#                    print((action["condition"].replace("value",str(self.value))))
#                    print(cond)
                    if not cond:
                        logger.debug("Condition not fulfilled")
                        return
                logger.info(f"Callback from {self.name}")
                if action["target"]==self.name:
                    logger.error(f"Circular reference in action {action}")
                    continue
                if action["type"]=="toggle":
                    self.dev_ht[action["target"]].toggle()
                elif action["type"]=="on":
                    self.dev_ht[action["target"]].set_value(1)
                elif action["type"]=="off":
                    self.dev_ht[action["target"]].set_value(0)
                elif action["type"]=="trigger":
                    self.dev_ht[action["target"]].trigger()
                elif action["type"]=="suspend":
                    self.dev_ht[action["target"]].suspended=True
                elif action["type"]=="unsuspend":
                    self.dev_ht[action["target"]].suspended=False
                elif action["type"]=="suspend_toggle":
                    self.dev_ht[action["target"]].suspended=not self.dev_ht[action["target"]].suspended
                elif action["type"]=="set_value":
                    newvalue=self.value
                    if "formula" in action:
                        newvalue=eval(action["formula"].replace("value",str(newvalue)))
                        print(newvalue)
                    self.dev_ht[action["target"]].set_value(newvalue)
                    
 
                    
        else:
            logger.debug(f"Debounce {self.name}")