import pyfirmata


class DigitalPin:
    DEFAULT_MODE = pyfirmata.OUTPUT

    def __init__(self, board, pin: int) -> None:
        self.pin = board.digital[pin]
        self.pin.mode = self.DEFAULT_MODE

    def set_mode(self, mode):
        self.pin.mode = mode

    def read(self):
        return self.pin.read()

    def write(self, state: float):
        return self.pin.write(state)


class AnalogPin:
    REFERENCE_VOLTAGE = 5

    def __init__(self, board, pin: int) -> None:
        self.pin = board.analog[pin]
        self.raw_value = None

    def enable_reporting(self):
        return self.pin.enable_reporting()

    def read(self):
        self.raw_value = self.pin.read()
        return self.raw_value

    def voltage(self):
        return (
            self.raw_value * AnalogPin.REFERENCE_VOLTAGE
            if self.raw_value is not None
            else None
        )

    def normalised_value(self, base: int = 100):
        return (
            (self.voltage() / AnalogPin.REFERENCE_VOLTAGE) * base
            if self.raw_value is not None
            else None
        )


class LED(DigitalPin):
    def on(self):
        return self.write(1)

    def off(self):
        return self.write(0)


class Buzzer(DigitalPin):
    DEFAULT_MODE = pyfirmata.PWM
    DEFAULT_ON_INTENSITY = 20
    DEFAULT_OFF_INTENSITY = 0

    def on(self):
        return self.write(Buzzer.DEFAULT_ON_INTENSITY)

    def off(self):
        return self.write(Buzzer.DEFAULT_OFF_INTENSITY)


class Button(DigitalPin):
    DEFAULT_MODE = pyfirmata.INPUT

    def is_pressed(self) -> bool:
        return self.read() == 1


class LightSensor(AnalogPin):
    def __init__(self, board, pin: int) -> None:
        super().__init__(board, pin)
        self.enable_reporting()


class PotentioMeter(AnalogPin):
    def __init__(self, board, pin: int) -> None:
        super().__init__(board, pin)
        self.enable_reporting()


class Board:
    def __init__(self, port: str, start_iterator: bool = False) -> None:
        self.board = pyfirmata.Arduino(port)
        print("Connected to board!")
        if start_iterator:
            pyfirmata.util.Iterator(self.board).start()

    def __enter__(self):
        return self.board

    def __exit__(self, *_):
        self.board.exit()
        print("\nFinished")
