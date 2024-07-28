#!/bin/bash
gst-launch-1.0 v4l2src device=/dev/video0 ! rtph264pay config-interval=10 pt=96 ! udpsink host=$1 port=5000 > /dev/null &

source .venv/bin/activate
python car_server.py 58008
