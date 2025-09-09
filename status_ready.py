from machine import Pin,I2C
import time
import vl53l0x
from vl53l0x import VL53L0X

SDA_PIN = 0
SCL_PIN = 1
XSHUT_PIN = 2
BUDGET_MS = 200
POLL_MS = 50

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

def raw_status(sensor):
    try:
        return sensor._read_u8(vl53l0x._RESULT_INTERRUPT_STATUS)
    except Exception:
        return None

def test_loop(sensor):
    while True:
        try:
            now = time.ticks_ms()
            ready = bool(sensor.data_ready)
            reg_before = raw_status(sensor)
            print(now, "ready", int(ready), "reg_before", reg_before)
            if ready:
                mm = sensor.read_range()
                reg_after = raw_status(sensor)
                print(" read:", mm, "reg_after", reg_after, "ready_after", int(bool(sensor.data_ready)))
            time.sleep_ms(POLL_MS)
        except Exception as e:
            print("err", e)
            time.sleep_ms(500)

if __name__ == "__main__":
    s = init_sensor()
    test_loop(s)

