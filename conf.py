configuration={
  "devices": [
    {
      "type": "textpanel",
      "name": "Text",
      "pin": 10,
      "config": {
          "i2c_addr" : 0x27,
          "i2c_num_rows" : 2,
          "i2c_num_cols" : 16
      }
    }
    ,
    {
       "type":"pinexpander",
       "name": "exp1",
       "pin":8,
       "config": {
          "i2c_addr" : 0x20
      }                 
    }
    ,
    {
       "type":"led",
       "name": "led1",
       "pin":1,
       "config": {
            "expander":"exp1",
            "mode": "blink",
            "blink_speed": 500,

      }                 
    }
    ,
    {
       "type":"led",
       "name": "led2",
       "pin":2,
       "config": {
            "expander":"exp1",
            "mode": "blink",
            "blink_speed": 1000,

      }                 
    }
    ,
    {
       "type":"led",
       "name": "led3",
       "pin":3,
       "config": {
            "expander":"exp1",
            "mode": "blink",
            "blink_speed": 2000,

      }                 
    }
    ,
    {
       "type":"led",
       "name": "led4",
       "pin":4,
       "config": {
            "expander":"exp1",
            "mode": "blink",
            "blink_speed": 3000,

      }                 
    }
    ,
    {
       "type":"led",
       "name": "led5",
       "pin":5,
       "config": {
            "expander":"exp1",
            "mode": "blink",
            "blink_speed": 4000,

      }                 
    }
  ]
}

