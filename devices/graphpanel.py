from logger import get_logger
from machine import Pin, Timer, I2C,SoftI2C
from utime import sleep,ticks_ms
from devices.device import Device
from drivers.ssd1306 import SSD1306_I2C

import gc

logger=get_logger()


class GraphPanel(Device):
    def __init__(self, dev_ht, name, pin,config):
        logger.info(f"Create TextPanel <{name}> Pin <{pin}>")
        super().__init__(dev_ht,name, pin,config)
        self.nextupdate=ticks_ms()+100
        self.sda=Pin(pin)
        self.i2c = SoftI2C(sda=self.sda, scl=Pin(pin+1), freq=400000)
        self.initialized=False
        self.poll_speed=100
        self.count=0
        self.values=[]

        try:
            self.oled_width = 128
            self.oled_height = 64
            self.oled = SSD1306_I2C(self.oled_width, self.oled_height, self.i2c)

            self.oled.text('Shingayki!', 0, 0)

            self.oled.show()
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
            self.oled.fill(0)
            self.count+=1
            
            F = gc.mem_free()
            A = gc.mem_alloc()
            T = F+A
            P='{0:.2f}%'.format(F/T*100)
            mem= ('Total:{0} Free:{1} ({2})'.format(T,F,P))
            self.oled.text(P, 0, 0)
#            self.lcd.putstr(P)
            
#            self.oled.pixel(self.count%128,self.count%64,1)
#            self.oled.framebuf.line(self.count%128,self.count%64,(-self.count%128),0,1)
            
            for value in self.values:
                x=int((ticks_ms()-value)/50)
                if x>128:
                    continue
                x2=int((ticks_ms()-value)/100)
                self.oled.framebuf.line(x,0,int(x**(3/2)),64,1)
                self.oled.framebuf.line(0,int(x2**(3/2)),128,x2,1)
                
            
            if len(self.values)>1:
                samples=len(self.values)
                if len(self.values)>4:
                    total=self.values[0]-self.values[4]
                    samples=5
                    
                else:
                    total=self.values[0]-self.values[-1]
                total2=(total/(samples-1))/1000
                #print(total2)
                total3=(60/total2)
                total3=int(total3)
#                total3=(total3*50)/60
                
#                self.oled.text(f'BPM {int(total3)}', 0, 20)
                mspeed=self.bpm_to_musical_speed(total3)
#                self.oled.text(f'Speed {mspeed}', 0, 30)
                self.oled.framebuf.rect(0,50,128,64,1,True)
                self.oled.framebuf.text(f'BPM {total3}',2,54,0)
                self.oled.framebuf.text(f'{mspeed}',64,54,0)
            else:
                self.oled.text(f'Click to start', 0, 20)
                
            self.oled.show()
        except Exception as e:
            logger.error("Unable to set oled")
            logger.error(e)
            
    def trigger(self):
        logger.info(f">>>Trigger:{ticks_ms()}")
        self.values.insert(0,ticks_ms())
        if len(self.values)>20:
            self.values=self.values[0:20]
            
        

    def run_old(self):
        if  not self.initialized:
            return
        if ticks_ms()<self.nextupdate:
           return
        try:
            self.nextupdate=ticks_ms()+self.poll_speed
            self.oled.fill(0)
            self.count+=1
            
            F = gc.mem_free()
            A = gc.mem_alloc()
            T = F+A
            P='{0:.2f}%'.format(F/T*100)
            mem= ('Total:{0} Free:{1} ({2})'.format(T,F,P))
            self.oled.text(P, 0, 20)
#            self.lcd.putstr(P)
            self.oled.pixel(self.count%128,self.count%64,1)
            self.oled.framebuf.line(self.count%128,self.count%64,(-self.count%128),0,1)
            self.oled.show()
        except Exception as e:
            logger.error("Unable to set oled")
            logger.error(e)
            
    def bpm_to_musical_speed(self,bpm):
        if bpm < 40:
            return "Grave"
        elif 40 <= bpm < 60:
            return "Largo"
        elif 60 <= bpm < 76:
            return "Adagio"
        elif 76 <= bpm < 108:
            return "Andante"
        elif 108 <= bpm < 120:
            return "Moderato"
        elif 120 <= bpm < 168:
            return "Allegro"
        elif 168 <= bpm < 200:
            return "Presto"
        else:
            return "Prestissimo"
            
