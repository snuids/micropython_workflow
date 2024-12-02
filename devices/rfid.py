from logger import get_logger
from machine import Pin, Timer, I2C
from utime import sleep,ticks_ms
from devices.device import Device
from drivers.mfrc522 import MFRC522

import ustruct
import math

logger=get_logger()


class RFID(Device):
    def __init__(self, dev_ht, name, pin,config):
        logger.debug(f"Create RFID <{name}> Pin <{pin}>")
        super().__init__(dev_ht,name, pin,config)
        self.actions=self.config.get("actions",[])
#        self.sda=Pin(pin)
        self.rfid=MFRC522(spi_id=0,sck=pin+1,miso=pin-1,mosi=pin+2,cs=pin,rst=22)
#        self.i2c = I2C(0, sda=self.sda, scl=Pin(pin+1), freq=400000)
        self.poll_speed=1000
        self.nextupdate=ticks_ms()+self.poll_speed
        
        self.value=0
        
#        self.data = bytearray(2)
        
    def run(self):
        if ticks_ms()<self.nextupdate:
           return
        try:
            self.rfid.init()
            self.nextupdate=ticks_ms()+self.poll_speed
            (stat, tag_type) = self.rfid.request(self.rfid.REQIDL)
            print(stat)
            if stat == self.rfid.OK:
                logger.debug("READ ON")
                (stat, uid) = self.rfid.SelectTagSN()
                if stat == self.rfid.OK:
                    card = int.from_bytes(bytes(uid),"little",False)
                    logger.debug("RFID ID: "+str(card))
                    self.value=str(card)
                    if self.rfid.IsNTAG():
                        logger.debug("Got NTAG{}".format(self.rfid.NTAG))
                        self.rfid.MFRC522_Dump_NTAG(Start=0,End=self.rfid.NTAG_MaxPage)
                        print
                        #print("Write Page 5  to 0x1,0x2,0x3,0x4  in 2 second")
                        #utime.sleep(2)
                        #data = [1,2,3,4]
                        #reader.writeNTAGPage(5,data)
                        #reader.MFRC522_Dump_NTAG(Start=5,End=6)
                    else:
                        logger.debug("Got REGULAR{}".format(self.rfid.NTAG))
                        (stat, tag_type) = self.rfid.request(self.rfid.REQIDL)
                        if stat == self.rfid.OK:
                            (stat, uid2) = self.rfid.SelectTagSN()
                            if stat == self.rfid.OK:
                                if uid != uid2:
                                    pass
                                defaultKey = [255,255,255,255,255,255]
                                self.rfid.MFRC522_DumpClassic1K(uid,Start=0, End=64, keyA=defaultKey)
                                print("TATA")
                    print("TATA")
                    self.callback(self.rfid.cs)
        except Exception as e:
            logger.error("Unable to compute RFID")
            logger.error(e)

