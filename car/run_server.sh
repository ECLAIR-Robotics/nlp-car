#!/bin/bash
gst-launch-1.0 libcamerasrc ! 'video/x-raw,width=640,height=480,framerate=30/1' ! videoconvert ! video/x-raw,format=NV12 ! v4l2h264enc extra-controls="controls,video_bitrate=2000000" ! 'video/x-h264,level=(string)4' ! h264parse config-interval=1 ! rtph264pay config-interval=1 pt=96 ! udpsink host=10.42.0.192 port=5000 > /dev/null &

# source .venv/bin/activate
python car_server.py 58008
