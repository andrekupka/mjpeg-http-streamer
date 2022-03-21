# mjpeg-http-streamer

![Build](https://github.com/andrekupka/mjpeg-http-streamer/actions/workflows/build-and-release,yaml/badge.svg)

A small python tool to create a MJPEG http stream from a plain mjpeg http stream.
Can be used in combination with `libcamera` on a Raspberry Pi to create a http stream for [OctoPrint](https://octoprint.org/).

Example invocation on a Raspian:

```bash
libcamera-vid -t 0 --inline --codec mjpeg -o - \
  | python3 -m mjpeg_http_streamer -l localhost -p 8080
```
