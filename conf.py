configuration={
  "devices": [
    {
      "type": "led",
      "name": "Green1",
      "pin": 0,
      "config": {
        "mode": "blink",
        "blink_speed": 500,
        "initial_state":0
      }
    },
    {
      "type": "led",
      "name": "Green2",
      "pin": 1,
      "config": {
        "auto_off_time": 1000,        
        "initial_state":0,
        "actions": [
          {
            "type": "on",
            "target": "Yellow1",
            "condition":"value==0"
          }
        ]
      }
    }
    ,
    {
      "type": "led",
      "name": "Yellow1",
      "pin": 2,
      "config": {
        "auto_off_time": 2000,
        "initial_state":0,
        "actions": [
          {
            "type": "on",
            "target": "Yellow2",
            "condition":"value==0"
          }
        ]
      }
    },
    {
      "type": "led",
      "name": "Yellow2",
      "pin": 3,    
      "config": {
        "initial_state":0,  
        "auto_off_time": 4000
      }
    },
    {
      "type": "sound",
      "name": "Sound1",
      "pin": 15,
      "config": {
        "actions": [
          {
            "type": "on",
            "target": "Green2"
          }
        ]
      }
    }
  ]
}

