import time
from machine import Pin, I2C
from vl53l0x import VL53L0X

SDA_PIN = 0
SCL_PIN = 1
XSHUT_PIN = 2
BUDGET_MS = 1000

def init_sensor():
    xshut = Pin(XSHUT_PIN, Pin.OUT)
    xshut.off()
    time.sleep_ms(20)
    xshut.on()
    time.sleep_ms(20)
    i2c = I2C(0, sda=Pin(SDA_PIN), scl=Pin(SCL_PIN), freq=400000)
    sensor = VL53L0X(i2c)
    sensor.measurement_timing_budget = BUDGET_MS * 1000
    sensor.start_continuous()
    return sensor

def wait_for_ready(sensor, deadline_ms):
    poll_ms = max(50, min(200, BUDGET_MS // 8))
    while not sensor.data_ready and time.ticks_diff(deadline_ms, time.ticks_ms()) > 0:
        time.sleep_ms(poll_ms)
    return bool(sensor.data_ready)

if __name__ == "__main__":
    sensor = init_sensor()
    next_tick = time.ticks_add(time.ticks_ms(), BUDGET_MS)
    while True:
        deadline = next_tick
        if wait_for_ready(sensor, deadline):
            try:
                mm = sensor.read_range()
                print(mm)
            except Exception as e:
                print("err", e)
        now = time.ticks_ms()
        next_tick = time.ticks_add(next_tick, BUDGET_MS)
        delay = time.ticks_diff(next_tick, now)
        if delay > 0:
            time.sleep_ms(delay)
        else:
            next_tick = time.ticks_add(time.ticks_ms(), BUDGET_MS)

