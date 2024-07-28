# nlp-car
NASCAR Language Processing!
ecar

## Setup
### Raspberry Pi

1. Install [GStreamer](https://gstreamer.freedesktop.org/documentation/installing/on-linux.html?gi-language=c)

2. Create and activate virtual environment:

`python -m venv .venv`

`source .venv/bin/activate`

3. Install required packages:

`pip install pigpio`

4. Enable the pigiod daemon:

`sudo systemctl enable pigpiod`

### Host Computer (Linux)

1. Install [GStreamer](https://gstreamer.freedesktop.org/documentation/installing/on-linux.html?gi-language=c) and [VLC](https://www.videolan.org/vlc/#download)

2. Open port 5000/udp:

On Fedora: `sudo firewall-cmd --add-port=5000/udp`

3. Create and activate virtual environment:

`python -m venv .venv`

`source .venv/bin/activate`

4. Install required packages:

`pip install pynput`

## Usage
### Raspberry Pi

Start server (default port for control is 58008 hehe, default port is 5000 for video stream):

`cd car`

`./run_server.sh <host computer IP>`

### Host Computer
Start client:

`cd control`

`./run_client.sh <Raspberry Pi IP>`

Use WASD to drive, hold space to go fast, Esc to exit. :D
