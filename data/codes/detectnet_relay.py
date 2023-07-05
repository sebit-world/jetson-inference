import jetson.inference
import jetson.utils

import argparse
import sys

import serial
import serial.tools.list_ports as ls_ports

PERSON_CLASS_ID = 1


def to_hex_cmd(pin, on):
    pin_base = int("A0", 16) + pin
    return f'A0{"%0.2X" % pin}{"%0.2X" % int(on)}{"%0.2X" % (pin_base + int(on))}'


def set_pin(device, pin, on, port=9600):
    with serial.Serial(device, port) as ser:
        ser.write(bytes.fromhex(to_hex_cmd(pin, on)))


def get_relay_device():
    ports = ls_ports.comports()
    for port in ports:
        if port.location:
            return port.device

# parse the command line
parser = argparse.ArgumentParser(description="Locate objects in a live camera stream using an object detection DNN.")

parser.add_argument("input_URI", type=str, default="", nargs='?', help="URI of the input stream")
parser.add_argument("output_URI", type=str, default="", nargs='?', help="URI of the output stream")
parser.add_argument("--network", type=str, default="ssd-mobilenet-v2", help="pre-trained model to load (see below for options)")
parser.add_argument("--overlay", type=str, default="box,labels,conf", help="detection overlay flags (e.g. --overlay=box,labels,conf)\nvalid combinations are:  'box', 'labels', 'conf', 'none'")
parser.add_argument("--threshold", type=float, default=0.5, help="minimum detection threshold to use") 

try:
    opt = parser.parse_known_args()[0]
except:
    print("")
    parser.print_help()
    sys.exit(0)

# load the object detection network
net = jetson.inference.detectNet(opt.network, sys.argv, opt.threshold)

# create video sources & outputs
input = jetson.utils.videoSource(opt.input_URI, argv=sys.argv)
output = jetson.utils.videoOutput(opt.output_URI, argv=sys.argv)

relay_device = get_relay_device()
set_pin(relay_device, 1, on=False)

# process frames until the user exits
while True:
    # capture the next image
    img = input.Capture()

    # detect objects in the image (with overlay)
    detections = net.Detect(img, overlay=opt.overlay)

    # render the image
    output.Render(img)

    ppl_count = 0
    for detection in detections:
        if detection.ClassID == PERSON_CLASS_ID:
            ppl_count += 1

    if ppl_count >= 1:
        set_pin(relay_device, 1, on=True)
    else:
        set_pin(relay_device, 1, on=False)

    # update the title bar
    output.SetStatus("{:s} | Network {:.0f} FPS".format(opt.network, net.GetNetworkFPS()))

    # print out performance info
    net.PrintProfilerTimes()

    # exit on input/output EOS
    if not input.IsStreaming() or not output.IsStreaming():
        break
