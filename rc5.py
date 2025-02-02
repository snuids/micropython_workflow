from utime import sleep,ticks_ms
import drivers.lcd_api
from machine import UART,Pin
from utime import sleep,ticks_ms

temp_on=False
temp_on_end=ticks_ms()
currentmode=0
lcd={}
kit=0
kits=[
    {"name":"Simple Beat","kit" :1}
    ,{"name":"Groove Beat","kit":1+4}
    ,{"name":"Rock","kit"       :1+4+7}
    ,{"name":"Funk","kit"       :1+4+7+4}
    ,{"name":"Shuffle","kit"    :1+4+7+4+4}
    ,{"name":"Swing","kit"      :1+4+7+4+4+5}
    ,{"name":"Side Stick","kit" :1+4+7+4+4+5+5}
    ,{"name":"Percus","kit"     :1+4+7+4+4+5+5+5}
    ,{"name":"Latin","kit"      :1+4+7+4+4+5+5+5+4}
    ,{"name":"Conga","kit"      :1+4+7+4+4+5+5+5+4+4}
    ,{"name":"Bossa","kit"      :1+4+7+4+4+5+5+5+4+4+3}    
    ,{"name":"Samba","kit"      :1+4+7+4+4+5+5+5+4+4+3+2}    
    ,{"name":"Dance Beat","kit"      :1+4+7+4+4+5+5+5+4+4+3+2+2}    
    
     ]
# ,CC#83#0
############ CONFIG
config={
  "modes": [
      {
          "mainline1":"      Rhythm",
          "mainline2":"      ------",
      "buttons":[
        {"command":"CC#83#{kit}",
            "lines":[
          "Kit      ",
          "{name}"
        ]},
        {"command":"CC#80#127,CC#80#0",
        "lines":[
          "Start",
          ""
        ]},
        {"command":"CC#81#127,CC#81#0",
        "lines":[
          "Stop",
          ""
        ]},
        {"command":"CC#82#127,CC#82#0",
            "lines":[
            "Tap Tempo",
            ""
        ]}
      ],
      "main": {
        "lines": [
          "< Kit          Tap >",
          "< Start       Stop >"
        ]
      }
    },
    {
        "mainline1":"      Tracks",
        "mainline2":"      ------",

      "buttons":[
        {"command":"CC#85#127,CC#85#0",
            "lines":[
          "< TRK          ",
          "Previous"
        ]},
        {},
        {},
        {"command":"CC#86#127,CC#86#0",
        "lines":[
          "               TRK >",
          "                Next"
        ]}
      ],
      "main": {
        "lines": [
          "< TRK          TRK >",
          ""
        ]
      }
    }
  ]
}

def set_text(lcd,text,line):
    text=(text+" "*20)[0:20]
#    print(f"==>{text} line={line}")
    lcd.lcd.move_to(0,line)
    lcd.lcd.putstr(text)
    

#midi = UART(0, baudrate=31250, bits=8, parity=None, stop=1, tx=Pin(12), rx=Pin(13), invert=0)
midi = UART(0, baudrate=31250, bits=8, parity=None, stop=1, tx=Pin(12), rx=Pin(13))

print(midi)

def run_rc5(devices_ht,led_onboard):
    global lcd,temp_on_end,temp_on 
    lcd=devices_ht["textpanel"]
    lcd.run=run_lcd
    lcd.call=call_lcd

    display_temp("> Midi Controller","> Starting",3)

    while True:
        sleep(0.1)
        led_onboard.toggle()
        for name,device in devices_ht.items():
            device.run()
        if temp_on and temp_on_end<ticks_ms():
            display_currentmode("main")
            temp_on=False
            
#        cc_1_on = b'\xb0\x01\x7f'
#        cc_1_off = b'\xb0\x01\x00'
#        midi.write(bytearray(cc_1_off))
#        midi.write(bytearray(cc_1_on))
   
            
def run_lcd():
    pass

def send_midi_control_change(channel, control, value):
    global midi
    status = 0xB0 | (channel & 0x0F)  # Control change message on the specified channel
    message = [status, control, value]
    print(message)
    midi.write(bytearray(message))
    
#    cc_1_on = b'\xb0\x01\x7f'
#    cc_1_off = b'\xb0\x01\x00'
    
#    midi.write(bytearray(cc_1_off))
#    midi.write(bytearray(cc_1_on))

# Send a control change message on channel 80 with value 127

def call_lcd(dev):
    global currentmode,kit,kits
    mode=config["modes"][currentmode]
    buttonindex=dev.config["number"]-1
    print("===>")
    print(buttonindex)
        
    if dev.config["number"]==5:
        currentmode=(currentmode+1)%(len(config["modes"]))
        display_currentmode("main")
    elif "buttons" in mode and buttonindex<len(mode["buttons"]) and "command" in mode["buttons"][buttonindex] \
                    and len(mode["buttons"][buttonindex]["command"])>0:
                
        
        display_temp(mode["buttons"][buttonindex]["lines"][0],
        mode["buttons"][buttonindex]["lines"][1],1)
        print("COMMAND"+mode["buttons"][buttonindex]["command"])
        commands=mode["buttons"][buttonindex]["command"].split(",")
        for commandfull in commands:
            print(commandfull)
            if "{kit}" in commandfull:
                kit+=1
                kit=kit%len(kits)
                display_temp(mode["buttons"][buttonindex]["lines"][0],
                mode["buttons"][buttonindex]["lines"][1].replace("{name}",kits[kit]["name"])
                             ,1)
                
            commandfull=commandfull.replace("{kit}",str(kits[kit]["kit"]))
            print(commandfull)

            command=commandfull.split('#')
            if command[0]=="CC":
                send_midi_control_change(1, int(command[1]), int(command[2]))  # Channel 80 corresponds to 79 (zero-indexed)

        

def display_temp(line1,line2,timeout):
    global temp_on_end,temp_on,lcd
    temp_on=True
    temp_on_end=ticks_ms()+(timeout*1000)
    set_text(lcd,line1, 0)
    set_text(lcd,line2, 3)


def display_currentmode(template):
    global config,lcd
    mode=config["modes"][currentmode]
    print(mode[template]["lines"][0])
    set_text(lcd,mode[template]["lines"][0], 0)
    set_text(lcd,mode[template]["lines"][1], 3)

    set_text(lcd,mode["mainline1"], 1)
    set_text(lcd,mode["mainline2"], 2)



#######