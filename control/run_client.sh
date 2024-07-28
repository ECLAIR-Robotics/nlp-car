#!/bin/bash
gst-launch-1.0 udpsrc uri=udp://$1:5000 ! rtph264depay ! openh264dec ! autovideosink > /dev/null &

vlc stream.sdp > /dev/null &

source .venv/bin/activate
python controller_client.py $1 58008