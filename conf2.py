configuration={
  "devices": [
    {
      "type": "led",
      "name": "Green1",
      "pin": 0
    },
    {
      "type": "led",
      "name": "Green2",
      "pin": 1      
    },
    {
      "type": "led",
      "name": "Yellow1",
      "pin": 2,
      "config": {
        "mode": "blink",
        "blink_speed": 500,
        "blink_off_speed": 1000,
      }
    },
    {
      "type": "led",
      "name": "Yellow2",
      "pin": 3,
      "config": {
        "mode": "blink",
        "blink_speed": 500,
        "blink_off_speed": 1000,        
        "initial_delay":200
      }
      
    },
    {
      "type": "led",
      "name": "Red1",
      "pin": 4,
      "config": {
        "mode": "blink",
        "blink_speed": 500,
        "blink_off_speed": 1000,        
        "initial_delay":400
      }
    },
    {
      "type": "led",
      "name": "Red2",
      "pin": 5,
      "config": {
        "initial_state": 0
      }
    },
    {
      "type": "switch",
      "name": "Switch1",
      "pin": 6,
      "config": {
        "actions": [
          {
            "type": "toggle",
            "target": "Green1"
          }
        ]
      }
    },
    {
      "type": "switch",
      "name": "Switch2",
      "pin": 7,
      "config": {
        "actions": [
          {
            "type": "toggle",
            "target": "Green2"
          }
        ]
      }
    },
    {
      "type": "switch",
      "name": "Switch4",
      "pin": 9,
      "config": {
        "actions": [
          {
            "type": "trigger",
            "target": "Servo2"
          }
        ]
      }
    },
    {
      "type": "servo",
      "name": "Servo1",
      "pin": 10,
      "config":{
          "mode": "random",
          "change_delay": 2000
        }
    },
    {
      "type": "servo",
      "name": "Servo2",
      "pin": 11,
      "config": {
        "mode": "sequence_switch",
        "sequence": [
          0,
          45,
          90,
          135,
          180
        ]
      }
    }
  ]
}
