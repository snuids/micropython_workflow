configuration={
  "devices": [
      {
      "type": "led",
      "name": "Yellow1",
      "pin": 1,
      "config": {
        "mode": "blink",
        "blink_speed": 500,
        "blink_off_speed": 1000,
      }
    },
      {
      "type": "switch",
      "name": "TapButton",
      "pin": 0
    }
    {
      "type": "graphpanel",
      "name": "OLED",
      "pin": 4,
      "config": {
          "i2c_addr" : 0x3c
      }
    }
    
  ]
}

