from machine import Pin, SoftI2C
from logger import get_logger

logger=get_logger()

def scan_i2c(sdapin,sclpin):
    i2c = SoftI2C(scl=Pin(sclpin), sda=Pin(sdapin))

    logger.info(f'Scanning sda={sdapin} scl={sclpin}')
    devices = i2c.scan()

    if len(devices) == 0:
      logger.info("No i2c device !")
    else:
      logger.info('i2c devices found:', len(devices))

      for device in devices:
        logger.info("Hexadecimal address: ", hex(device))
