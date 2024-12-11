import network
from time import sleep
from logger import get_logger
from umqtt.robust import MQTTClient

logger=get_logger()

def initialize_wifi(ssid, password):
    logger.info(f"SSID:{ssid}")
    wlan = network.WLAN(network.STA_IF)
    sleep(1)
    logger.info(f"SSID:{ssid} {password}")    
    wlan.active(True)
    logger.info("WLAN Active:",wlan.active())

#    networks = wlan.scan()
#    print(networks)
    # Connect to the network
    wlan.connect(ssid, password)
    # Wait for Wi-Fi connection
    connection_timeout = 10
    while connection_timeout > 0:
        if wlan.status() >= 3:
            return True
            break
        connection_timeout -= 1
        print('Waiting for Wi-Fi connection...')
        sleep(1)
    return False

def connect_mqtt(client_id,host,port,user,password):
    try:
        client = MQTTClient(client_id=client_id,
                            server=host,
                            port=port,
                            user=user,
                            password=password,
                            keepalive=60,ssl=False)#,
#                            ssl=MQTT_SSL,
#                            ssl_params=MQTT_SSL_PARAMS)
        client.connect()
        return client
    except Exception as e:
        print('Error connecting to MQTT:', e)
        raise  # Re-raise the exception to see the full traceback

