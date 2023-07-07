"""Demo3: using button to switch ON / OFF Buzzer"""
import time
from base import Buzzer, PotentioMeter, Board, Button


POTENTIO_METER_PIN = 0
BUZZER_PIN = 5
PORT = "/dev/ttyUSB0"

if __name__ == "__main__":
    with Board(PORT, start_iterator=True) as board:
        potential_meter = PotentioMeter(board, POTENTIO_METER_PIN)
        buzzer = Buzzer(board, BUZZER_PIN)
        button = Button(board, 4)
        buzzing = False
        while 1:
            try:
                if button.is_pressed():
                    if not buzzing:
                        print("BUZZZZZ!!")
                        buzzer.on()
                        buzzing = True
                elif buzzing:
                    print("STOP!")
                    buzzer.off()
                    buzzing = False
                time.sleep(0.01)
            except KeyboardInterrupt:
                break
