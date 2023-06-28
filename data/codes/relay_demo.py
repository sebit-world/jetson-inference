from time import sleep
import serial
import serial.tools.list_ports as ls_ports


def to_hex_cmd(pin, on):
    pin_base = int("A0", 16) + pin
    if on:
        return f'A0{"%0.2X" % pin}01{"%0.2X" % (pin_base + 1)}'
    else:
        return f'A0{"%0.2X" % pin}00{"%0.2X" % pin_base}'


def set_pin(device, pin, on, port=9600):
    with serial.Serial(device, port) as ser:
        ser.write(bytes.fromhex(to_hex_cmd(pin, on)))


if __name__ == "__main__":
    ports = ls_ports.comports()
    for port in ports:
        if port.location:
            set_pin(port.device, 1, on=True)
            sleep(0.15)
            set_pin(port.device, 1, on=False)
            sleep(0.15)
            
            set_pin(port.device, 2, on=True)
            sleep(0.15)
            set_pin(port.device, 2, on=False)
            sleep(0.15)
