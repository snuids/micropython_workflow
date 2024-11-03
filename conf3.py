configuration={
  "devices": [
    {
      "type": "led",
      "name": "Green1",
      "pin": 0,
      "config": {
        "mode": "blink",
        "blink_speed": 500
        }

    },
    {
      "type": "led",
      "name": "Green2",
      "pin": 1,
            "config": {
        "mode": "blink",
        "blink_speed": 500,
        "initial_delay":200
        }
    }
    ,
    {
      "type": "led",
      "name": "Yellow1",
      "pin": 2,
        "config": {
        "mode": "blink",
        "blink_speed": 500,
        "initial_delay":400
        }
    },
    {
      "type": "led",
      "name": "Yellow2",
      "pin": 3
      
    },
    {
      "type": "switch",
      "name": "BoutonVert",
      "pin": 6,
      "config": {
        "actions": [
          {
            "type": "toggle",
            "target": "Yellow2"
          },
          {
            "type": "suspend_toggle",
            "target": "Green1"
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
      "pin": 10
    }
    ,
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
    ,
    {
      "type": "ultrasonic",
      "name": "Sonic",
      "pin": 14,
      "config": {
        "actions": [
          
          {
            "type": "set_value",
            "target": "Servo1",
            "condition":"value<120",
            "formula":"value*4"
          }

        ]
      }
      
    }
    
    ]
}