configuration={
  "devices": [
    {
      "type": "led",
      "name": "RedLed",
      "pin": 3,
      "config": {
        "mode": "solid",
        "auto_off_time":2000
        

      }
    },
    {
      "type": "led",
      "name": "GreenLed",
      "pin": 2,
      "config": {
        "mode": "blink"

      }
    },  
    {
      "type": "servo",
      "name": "ServoOpen",
      "pin": 17,
      "config": {
        "mode": "trigger",
        "initial_state":50,
        "return_to_intial_delay":1

      }
    },
    {
      "disabled":True,
      "type": "battery",
      "name": "Battery",
      "pin": 2,
        "config": {
      }
    },    
    {
      "type": "switch",
      "name": "SwitchOpen",
      "pin": 4,
      "config": {
        "actions": [
          {
            "type": "set_value",
            "target": "ServoOpen",
            "formula":"0"
          },
          {
            "type": "set_value",
            "target": "RedLed",
            "formula":"1"
          }
        ]
      }
    }
    ,{
                "disabled":True,
      "type": "voltagereader",
      "name": "Volt",
      "pin": 28,
      "config": {

          "poll_speed":30000,
          "actions": [
          {
            "type": "set_value",
            "target": "Battery",
          }
        ]
      }
    }
    
    ]
}
