from utime import sleep,ticks_ms




def run_lidar(devices_ht,led_onboard):
    servo1=devices_ht["Servo1"]
    servo2=devices_ht["Servo2"]
    sonic=devices_ht["Sonic"]
    tof=devices_ht["TimeOfFlight"]

    filename="/data.txt"
    with open(filename, 'w') as file:
        pass
    
    for r in range(0,150,1):
        servo1.set_value(r)
        values=""
        for teta in range(10,150,1):
            servo2.set_value(teta)
            sonic.reset()
            sonic.run()
            tof.reset()
            tof.run()
            print(f">{r};{teta};{sonic.value};{tof.value};")
            values+=f"{r};{teta};{sonic.value};{tof.value};\n"
            sleep(0.01)
        with open(filename, 'a') as file:
            file.write(values)
            
    A/0
        
        
    
    while True:
        sleep(0.1)
        led_onboard.toggle()
        for name,device in devices_ht.items():
            device.run()
