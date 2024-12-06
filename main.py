from machine import Pin, Timer
from conf import configuration
from utime import sleep,ticks_ms
from logger import get_logger
from devices.switch import Switch
from devices.servo import Servo
from devices.led import Led
from devices.ultrasonic import UltraSonic
from devices.sound import Sound
from devices.accelerometer import Accelerometer
from devices.textpanel import TextPanel
from devices.graphpanel import GraphPanel
from devices.pinexpansion import PinExpander
from devices.voltagereader import *
from devices.tof import TimeOfFlight
from devices.rfid import RFID
from devices.battery import Battery
from debug.scani2c import scan_i2c

#import micropython
#micropython.alloc_emergency_exception_buf(100)

import devices
device_classes={}
for name, obj in globals().items():
    if isinstance(obj, type) and issubclass(obj, Device):
#        print(obj.__name__)
        device_classes[obj.__name__.lower()]=obj
#        print(obj)

#print(device_classes)

logger=get_logger()
logger.set_level("DEBUG")

from wifi import wifi_secret
from drivers.wifi import initialize_wifi

#if not initialize_wifi(wifi_secret["ssid"], wifi_secret["pass"]):
#    logger.error('Error connecting to the network... exiting program')

CUBE=False
LIDAR=False

if CUBE:
    logger.info("CUBE CONFIG")
    logger.info("===========")
    from cube import create_cube_configuration
    create_cube_configuration(configuration)

devices_ht={}

logger.debug(configuration)

#scan_i2c(8,9)
#scan_i2c(4,5)

# check config
pin_ht={}
name_ht={}
for device in configuration["devices"]:
    if "expander" in device:
        continue
    if device["pin"] in pin_ht:
        logger.error(f"Bad Config pin <{device['pin']}>") # pin used twice
    pin_ht[device["pin"]]=True
    if device["name"] in name_ht:
        logger.error(f"Bad Config name <{device['name']}>") # name used twice
    name_ht[device["name"]]=True
        

# instantiate devices
for device in configuration["devices"]:
    logger.debug(device)
    if device["type"] in device_classes:
        devices_ht[device["name"]]=device_classes[device["type"]](devices_ht,device["name"],device["pin"],device.get("config",{}))               
    else:
        logger.error(f'Unknown type <{device["type"]}>')
    
# set expansions

for name,device in devices_ht.items():
    if "expander" in device.config:
        if device.config["expander"] not in devices_ht:
            logger.error(f"Unknown expander {device.config}")
        else:
            device.expander=devices_ht[device.config["expander"]]
        
led_onboard = Pin(25, Pin.OUT)

if CUBE:
    logger.info("RUN CUBE")
    logger.info("===========")
    from cube import run_cube
    run_cube(devices_ht,led_onboard)


if LIDAR:
    logger.info("RUN LIDAR")
    from lidar import run_lidar
    run_lidar(devices_ht,led_onboard)

while True:
    sleep(0.1)
    led_onboard.toggle()
    for name,device in devices_ht.items():
        device.run()
        
    
    