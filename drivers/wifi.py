import network
from time import sleep
from logger import get_logger

logger=get_logger()

def initialize_wifi(ssid, password):
    logger.info(f"SSID:{ssid} {password}")
    wlan = network.WLAN(network.STA_IF)
    sleep(1)
    logger.info(f"SSID:{ssid} {password}")    
    wlan.active(True)
    logger.info("WLAN Active:",wlan.active())
    print("totot")

    # Connect to the network
    wlan.connect(ssid, password)
    print("totot2")
    # Wait for Wi-Fi connection
    connection_timeout = 10
    while connection_timeout > 0:
        if wlan.status() >= 3:
            break
        connection_timeout -= 1
        print('Waiting for Wi-Fi connection...')
        sleep(1)