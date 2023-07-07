import jetson.inference
import jetson.utils

import argparse
import sys

from base import Board, LED

# parse the command line
parser = argparse.ArgumentParser(
    description="Locate objects in a live camera stream using an object detection DNN."
)

parser.add_argument(
    "input_URI", type=str, default="", nargs="?", help="URI of the input stream"
)
parser.add_argument(
    "output_URI", type=str, default="", nargs="?", help="URI of the output stream"
)
parser.add_argument(
    "--network",
    type=str,
    default="ssd-mobilenet-v2",
    help="pre-trained model to load (see below for options)",
)
parser.add_argument(
    "--overlay",
    type=str,
    default="box,labels,conf",
    help="detection overlay flags (e.g. --overlay=box,labels,conf)\nvalid combinations are:  'box', 'labels', 'conf', 'none'",
)
parser.add_argument(
    "--threshold", type=float, default=0.5, help="minimum detection threshold to use"
)

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


# process frames until the user exits
with Board("/dev/ttyUSB0", True) as board:
    led = LED(board, 6)
    while True:
        # capture the next image
        img = input.Capture()

        # detect objects in the image (with overlay)
        detections = net.Detect(img, overlay=opt.overlay)

        count = 0
        for detection in detections:
            if detection.ClassID == 1:
                count += 1

        # render the image
        output.Render(img)
        if count >= 1:
            led.on()
        else:
            led.off()
        # update the title bar
        output.SetStatus(
            "{:s} | Network {:.0f} FPS".format(opt.network, net.GetNetworkFPS())
        )

        # print out performance info
        net.PrintProfilerTimes()

        # exit on input/output EOS
        if not input.IsStreaming() or not output.IsStreaming():
            break
