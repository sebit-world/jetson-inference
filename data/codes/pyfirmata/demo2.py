"""Demo2: using Potentiometer to switch LED brightness"""
import time
import pyfirmata
from base import PotentioMeter, Board, LED


PIN = 0
BUZZER_PIN = 6
PORT = "/dev/ttyUSB0"

if __name__ == "__main__":
    with Board(port=PORT, start_iterator=True) as board:
        potentio_meter = PotentioMeter(board, PIN)
        led = LED(board, BUZZER_PIN)
        led.set_mode(pyfirmata.PWM)
        prev_value = None
        while 1:
            try:
                potentio_meter.read()
                value = potentio_meter.normalised_value(1)
                if value is not None and value != prev_value:
                    print(value)
                    led.write(value)
                    prev_value = value
                time.sleep(0.01)
            except KeyboardInterrupt:
                break
