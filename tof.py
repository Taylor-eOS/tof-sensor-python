from machine import Pin, I2C
import time
from vl53l0x import VL53L0X

SDA_PIN = 0
SCL_PIN = 1
XSHUT_PIN = 2
BUDGET_MS = 1000

xshut = Pin(XSHUT_PIN, Pin.OUT)
xshut.off()
time.sleep_ms(20)
xshut.on()
time.sleep_ms(20)
i2c = I2C(0, sda=Pin(SDA_PIN), scl=Pin(SCL_PIN), freq=400000)
sensor = VL53L0X(i2c)
sensor.measurement_timing_budget = BUDGET_MS * 1000
sensor.start_continuous()
while True:
    if sensor.data_ready:
        mm = sensor.read_range()
        print(mm)

