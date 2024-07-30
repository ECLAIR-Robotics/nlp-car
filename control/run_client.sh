#!/bin/bash
gst-launch-1.0 udpsrc uri=udp://$1:5000 ! rtph264depay ! openh264dec ! autovideosink > /dev/null &

address=$(ip addr | grep 'state UP' -A2 | tail -n1 | awk '{print $2}' | cut -f1  -d'/')
sed -i 's/^c=.*/c=IN IP4 '$address'/g' stream.sdp

vlc stream.sdp > /dev/null &

source .venv/bin/activate
python controller_client.py $1 58008