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
        self.actions=self.config.get("actions",[])
        self.parameters=[]
        self.expander=None
    
    def reset(self):
        self.nextupdate=ticks_ms()-1    
    
    def run(self):
        pass

    def resolve_formula(self,formula):
        if len(self.parameters)==0:
            formula=formula.replace("value",str(self.value))
        else:
            for param in self.parameters:
                formula=formula.replace(param,str(getattr(self,param)))
        return formula
            
            

    def callback(self,pin):

        logger.debug(f"Callback {self}")
        if ticks_ms()>self.next_callback or self.__class__.__name__!="UltraSonic":
            self.next_callback=ticks_ms()+self.debounce_delay
            for action in self.actions:                
                logger.debug(f"Execute {action}")
                if "condition" in action:
                    cond=eval(self.resolve_formula(action["condition"]))
#                    print((action["condition"].replace("value",str(self.value))))
#                    print(cond)
                    if not cond:
                        logger.debug("Condition not fulfilled")
                        return
                logger.info(f"Callback from {self.name}")
                if action["target"]==self.name:
                    logger.error(f"Circular reference in action {action}")
                    continue
                
                if action["target"] not in self.dev_ht:
                    logger.error(f"Unknown target {action['target']}")

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
                    if "formula" in action:
                        newvalue=eval(self.resolve_formula(action["formula"]))
                    else:
                        newvalue=self.value
                    print(newvalue)
                    self.dev_ht[action["target"]].set_value(newvalue)
                    
 
                    
        else:
            logger.debug(f"Debounce {self.name}")
