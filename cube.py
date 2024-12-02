from logger import get_logger
from utime import sleep,ticks_ms
import json

logger=get_logger()

def create_cube_configuration(configuration):
    logger.info("Create Layers as led")
    for i in range(0,5):
        newled={
              "type": "led",
              "name": f"Layer{i}",
              "pin": 12+i
            }
        configuration["devices"].append(newled)
    
    for i in range(0,8):
        target=i
            
            
        newled={
              "type": "led",
              "name": f"Pos{target}",
              "pin": i+1,
              "config":{
                  "expander":"Expander1"
              }
              
            }
        configuration["devices"].append(newled)
        newled={
              "type": "led",
              "name": f"Pos{i+8}",
              "pin": i+1,
              "config":{
                  "expander":"Expander2"
              } 
            }
        configuration["devices"].append(newled)
    logger.info(json.dumps(configuration["devices"]))
    
    
def set_layer(layer,turnon):
    if turnon:
        layer[0]["y"].set_value(0)
        for i in range(0,16):
            layer[i]["x"].set_value(1)
    else:
        layer[0]["y"].set_value(1)
        for i in range(0,16):
            layer[i]["x"].set_value(0)
            
            



def run_cube(devices_ht,led_onboard):
    logger.info("In Cube Running")
    logger.info(json.dumps(devices_ht))
    # create cube layers
    
    layers=[]
    for i in range(0,4):
        layer=[]
        for j in range(0,16):
            led={"x":devices_ht[f"Pos{j}"],"y":devices_ht[f"Layer{i}"]}
            layer.append(led)    
        layers.append(layer)
    
    for i in range(0,4):
        set_layer(layers[i],False)

#    set_layer(layers[0],True)
#    sleep(3)
#    set_layer(layers[0],False)
#    set_layer(layers[1],True)
#    layers[0][0]["y"].set_value(0)
    layers[1][0]["y"].set_value(0)
    layers[2][0]["y"].set_value(0)    
#    layers[2][0]["y"].set_value(0)
    layers[1][1]["x"].set_value(1)
    
        
#    sleep(30)


    
    while True:

            

        if True:  # ROTATE
            for curlayer in range(0,4):
                speed=0.8/(curlayer+1)
                for i in range(0,4):
                    layers[i][0]["y"].set_value(1)
                    
                layers[curlayer][0]["y"].set_value(0)
                    
                for i in range(0,16):
                    layers[0][i]["x"].set_value(0)
                    
                layers[0][0]["x"].set_value(1)
                layers[0][1]["x"].set_value(1)
                layers[0][2]["x"].set_value(1)
                layers[0][3]["x"].set_value(1)            
                
                sleep(speed)
                
                layers[0][1]["x"].set_value(1)
                layers[0][2]["x"].set_value(0)
                layers[0][6]["x"].set_value(1)
                layers[0][3]["x"].set_value(0)            
                layers[0][7]["x"].set_value(1)            

                sleep(speed)
                
                layers[0][1]["x"].set_value(0)
                layers[0][5]["x"].set_value(1)
                layers[0][6]["x"].set_value(0)
                layers[0][10]["x"].set_value(1)
                layers[0][7]["x"].set_value(0)
                layers[0][15]["x"].set_value(1)                        

                sleep(speed)
                
                layers[0][1]["x"].set_value(0)
                layers[0][5]["x"].set_value(0)
                layers[0][4]["x"].set_value(1)            
                layers[0][10]["x"].set_value(0)
                layers[0][9]["x"].set_value(1)
                layers[0][15]["x"].set_value(0)                        
                layers[0][13]["x"].set_value(1)                        
                sleep(speed)

                layers[0][1]["x"].set_value(0)
                layers[0][5]["x"].set_value(0)
                layers[0][4]["x"].set_value(1)            
                layers[0][9]["x"].set_value(0)
                layers[0][8]["x"].set_value(1)
                layers[0][13]["x"].set_value(0)                        
                layers[0][12]["x"].set_value(1)                        
                sleep(speed)
                
            


        if True:  # UP DOWN
            
            for i in range(0,16):
                layers[0][i]["x"].set_value(1)

            for curlayer in range(0,8):
                for i in range(0,4):
                    set_layer(layers[i],False)
                set_layer(layers[curlayer%4],True)
                sleep(0.2)
                
            for i in [0,1,2,3,4,7,8,11,12,13,14,15]:
                layers[0][i]["x"].set_value(0)

            for curlayer in range(0,8):
                for i in range(0,4):
                    layers[i][0]["y"].set_value(1)
#                    set_layer(layers[i],False)
                layers[curlayer%4][0]["y"].set_value(0)
#                set_layer(layers[curlayer%4],True)
                sleep(0.2)
                
            
            for i in range(0,16):
                layers[0][i]["x"].set_value(0)

            for i in [0,1,2,3,4,7,8,11,12,13,14,15]:
                layers[0][i]["x"].set_value(1)

            for curlayer in range(0,8):
                for i in range(0,4):
                    layers[i][0]["y"].set_value(1)
#                    set_layer(layers[i],False)
                layers[curlayer%4][0]["y"].set_value(0)
#                set_layer(layers[curlayer%4],True)
                sleep(0.2)
                
                    
        def compute_target(y):
            targ=y
            if y>=4 and y<=7:
                targ=7-y+4

            if y>=12 and y<=15:
                targ=15-y+12
                
            if y<=0:
                targ=0
                
            return targ
                
            
            

        if True:
            for x in range(0,4):
                speed=0.5/(x+1)
                for i in range(0,4):
                    if i==x:
                        layers[i][0]["y"].set_value(0)
                    else:
                        layers[i][0]["y"].set_value(1)

                for y0 in range(0,16):
                    if x%2==0:                        
                        y=y0
                    else:
                        y=15-y0
                    for i in range(0,16):
                        layers[0][i]["x"].set_value(0)
                    targ=compute_target(y)
                    targ2=compute_target(y-1)
                    targ3=compute_target(y-2)
                    
                    layers[0][targ]["x"].set_value(1)
                    layers[0][targ2]["x"].set_value(1)                    
                    layers[0][targ3]["x"].set_value(1)                    
                    sleep(speed)
            

 
            
            
        

#        for name,device in devices_ht.items():
#            device.run()
    
