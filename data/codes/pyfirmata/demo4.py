"""Demo4: Turn on LED if brightness less than a threshold"""
import time

from base import LED, LightSensor, Board

LIGHT_SENSOR_PIN = 3
LED_PIN = 6
PORT = "/dev/ttyUSB0"

if __name__ == "__main__":
    with Board(PORT, start_iterator=True) as board:
        light_sensor = LightSensor(board, LIGHT_SENSOR_PIN)
        led = LED(board, LED_PIN)
        while 1:
            try:
                light_sensor.read()
                brightness = light_sensor.normalised_value(1)
                print(brightness)
                if brightness is not None and brightness < 0.05:
                    led.on()
                else:
                    led.off()
                time.sleep(0.5)
            except KeyboardInterrupt:
                break
