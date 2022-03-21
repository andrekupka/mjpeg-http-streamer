import asyncio
import sys

from src.mjpeg_http_streamer.app import make_app, run_app
from src.mjpeg_http_streamer.arguments import parse_arguments
from src.mjpeg_http_streamer.frame_broker import FrameBroker
from src.mjpeg_http_streamer.stream_provider import InstantStreamProvider, ClockedStreamProvider
from src.mjpeg_http_streamer.mjpeg_frame_reader import MJPEGStreamReader


async def create_stdin_stream():
    loop = asyncio.get_event_loop()
    reader = asyncio.StreamReader()
    protocol = asyncio.StreamReaderProtocol(reader)
    await loop.connect_read_pipe(lambda: protocol, sys.stdin)
    return reader


def create_stream_provider(stream, args):
    clocked = args.clocked
    if clocked is None:
        return InstantStreamProvider(stream)
    return ClockedStreamProvider(stream, interval=clocked/1000)


async def main():
    args = parse_arguments()
    print(args)

    frame_queue = asyncio.Queue()

    stream_provider = create_stream_provider(await create_stdin_stream(), args)

    stream_reader = MJPEGStreamReader(stream_provider, frame_queue)
    frame_broker = FrameBroker(frame_queue)
    app = make_app(frame_broker)

    await asyncio.gather(
        run_app(app, args.listen, args.port),
        stream_reader.run(),
        frame_broker.run(),
    )


asyncio.run(main())
