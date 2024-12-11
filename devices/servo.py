# Based on Rui Santos & Sara Santos - Random Nerd Tutorials

from machine import Pin, PWM
from logger import get_logger
from random import randint
from utime import sleep,ticks_ms
from devices.device import Device

logger=get_logger()

class Servo(Device):

    __servo_pwm_freq = 50
    __min_u16_duty = 1802
    __max_u16_duty = 7864
    min_angle = 0
    max_angle = 180
    current_angle = 0.001
    curseq=0


    def __init__(self,dev_ht, name,pin,config):
        logger.debug(f"Create Servo <{name}> Pin <{pin}>")
        super().__init__(dev_ht,name, pin,config)
        self.mode=self.config.get("mode","fixed")
        self.__initialise(pin)
        self.initial_state=self.config.get("initial_state",0)
        self.move(self.initial_state)
        self.return_to_intial_delay=self.config.get("return_to_intial_delay",0)
        self.change_delay=self.config.get("change_delay",1000)
        self.last_change=ticks_ms()
        self.nextupdate=ticks_ms()+self.change_delay


    def update_settings(self, servo_pwm_freq, min_u16_duty, max_u16_duty, min_angle, max_angle, pin):
        self.__servo_pwm_freq = servo_pwm_freq
        self.__min_u16_duty = min_u16_duty
        self.__max_u16_duty = max_u16_duty
        self.min_angle = min_angle
        self.max_angle = max_angle
        self.__initialise(pin)


    def move(self, angle):
        # round to 2 decimal places, so we have a chance of reducing unwanted servo adjustments
        angle = round(angle, 2)
        # do we need to move?
        if angle == self.current_angle:
            return
        logger.debug(f"Set Angle To:{angle}")
        self.last_change=ticks_ms()
        self.current_angle = angle
        # calculate the new duty cycle and move the motor
        duty_u16 = self.__angle_to_u16_duty(angle)
        self.__motor.duty_u16(duty_u16)
    
    def stop(self):
        self.__motor.deinit()
    
    def get_current_angle(self):
        return self.current_angle

    def __angle_to_u16_duty(self, angle):
        return int((angle - self.min_angle) * self.__angle_conversion_factor) + self.__min_u16_duty

    def trigger(self):
        if self.mode=="random_switch":
            newangle=randint(0,180)
            logger.debug(f"Servo <{self.name}> Set new angle <{newangle}>")
            self.move(newangle)
        elif self.mode=="sequence_switch":
            self.curseq+=1
            if self.curseq>=len(self.config["sequence"]):
                self.curseq=0
                
            newangle=self.config["sequence"][self.curseq]
            logger.debug(f"Servo <{self.name}> Set new angle <{newangle}>")
            self.move(newangle)
        elif self.mode=="set_value":
            self.move(newangle)
        else:
            logger.error(f"Unknown mode <{self.mode}>")




    def run(self):
        if self.mode=="random":
            if ticks_ms()>self.nextupdate:
                self.nextupdate=ticks_ms()+self.change_delay
                newangle=randint(0,180)
                logger.debug(f"Servo <{self.name}> Set new angle <{newangle}>")
                self.move(newangle)
        if self.return_to_intial_delay>0 and self.last_change+(self.return_to_intial_delay*1000)<ticks_ms() and self.current_angle!=self.initial_state:
            logger.info(f"{self} Return to inital state")
            self.move(self.initial_state)

    def set_value(self,value):
        self.move(value)

    def __initialise(self, pin):
        self.current_angle = -0.001
        self.__angle_conversion_factor = (self.__max_u16_duty - self.__min_u16_duty) / (self.max_angle - self.min_angle)
        self.__motor = PWM(Pin(pin))
        self.__motor.freq(self.__servo_pwm_freq)