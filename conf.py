configuration={
  "devices": [
    {
      "type": "led",
      "name": "Left",
      "pin": 0,
      "config": {
        "initial_state":1,
        "auto_off_time": 3000
      }
    },
    {
      "type": "led",
      "name": "Center",
      "pin": 1,
      "config": {
        "initial_state":1,
        "auto_off_time": 3000
      }
    },
    {
      "type": "led",
      "name": "Right",
      "pin": 2,
      "config": {
        "initial_state":1,
        "auto_off_time": 3000
      }
    },
    {
      "type": "switch",
      "name": "SwitchGreen",
      "pin": 10,
      "config": {
        "actions": [
          {
            "type": "on",
            "target": "Left"
          }
          ,{
            "type": "off",
            "target": "Center"
          },
          {
            "type": "off",
            "target": "Right"
          }
        ]
      }
    }
    ,    
    {
      "type": "switch",
      "name": "SwitchYellow",
      "pin": 11,
      "config": {
        "actions": [
          {
            "type": "off",
            "target": "Left"
          }
          ,{
            "type": "on",
            "target": "Center"
          },
          {
            "type": "off",
            "target": "Right"
          }
        ]
      }
    }
    ,    
    {
      "type": "switch",
      "name": "SwitchRed",
      "pin": 12,
      "config": {
        "actions": [
          {
            "type": "off",
            "target": "Left"
          }
          ,{
            "type": "off",
            "target": "Center"
          },
          {
            "type": "on",
            "target": "Right"
          }        ]
      }     
    }
    ,    
    {
      "type": "switch",
      "name": "SwitchRed",
      "pin": 13,
      "config": {
        "actions": [
          {
            "type": "on",
            "target": "Left"
          }
          ,{
            "type": "on",
            "target": "Center"
          },
          {
            "type": "on",
            "target": "Right"
          }        ]
      }     
    }
  ]
}



