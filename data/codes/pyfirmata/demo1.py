"""Demo1: using button to switch ON / OFF LED"""
import time
from base import LED, Button, Board


LED_PIN = 6
BUTTON_PIN = 4
DEFAULT_PORT = "/dev/ttyUSB0"


def main():
    with Board(DEFAULT_PORT, True) as board:
        led = LED(board, 6)
        button = Button(board, 4)
        print("Try press the button & observe the LED")
        while 1:
            try:
                if button.is_pressed():
                    led.on()
                else:
                    led.off()
                time.sleep(0.01)
            except KeyboardInterrupt:
                break


if __name__ == "__main__":
    main()
