from machine import Pin, I2C
import time

xshut = Pin(2, Pin.OUT)
xshut.off()
time.sleep_ms(20)
xshut.on()
time.sleep_ms(20)
i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=400000)
#i2c = I2C(0, sda=Pin(4), scl=Pin(5), freq=400000)

from vl53l0x import VL53L0X
sensor = VL53L0X(i2c)

while True:
    try:
        mm = sensor.range
        print(mm)
    except Exception as e:
        print("err",e)
    time.sleep_ms(200)

