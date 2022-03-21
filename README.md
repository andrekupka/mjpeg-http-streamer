# mjpeg-http-streamer

![Build](https://github.com/andrekupka/mjpeg-http-streamer/actions/workflows/build-and-release.yaml/badge.svg)
![Release](https://img.shields.io/github/v/release/andrekupka/mjpeg-http-streamer)

A small python tool that reads a plain MJPEG stream from `stdin` and publishes it as http MJPEG stream.
It can be used in combination with `libcamera` on a Raspberry Pi to create a http stream for [OctoPrint](https://octoprint.org/).

## Installation

Installation is done via `pip`.

```bash
pip install mjpeg-http-streamer
```

## Usage

Example invocation on a Raspberry PI:

```bash
libcamera-vid -t 0 --inline --codec mjpeg -o - \
  | python3 -m mjpeg_http_streamer -l <host> -p 8080
```

The HTTP stream can be received by opening the url `http://<host>:8080/stream`.
Further a single snapshot can be retrieved using `http://<host>:8080/snapshot`.

In production use cases it is advised to host `mjpeg-http-streamer` behind a reverse proxy like nginx.