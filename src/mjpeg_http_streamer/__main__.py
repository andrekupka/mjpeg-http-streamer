import asyncio

from mjpeg_http_streamer.app import make_app, run_app
from mjpeg_http_streamer.arguments import parse_arguments
from mjpeg_http_streamer.frame_broker import FrameBroker
from mjpeg_http_streamer.mjpeg_frame_reader import MJPEGStreamReader
from mjpeg_http_streamer.source import create_input_source
from mjpeg_http_streamer.stream_provider import InstantStreamProvider, ClockedStreamProvider


def create_stream_provider(source, args):
    clocked = args.clocked
    if clocked is None:
        return InstantStreamProvider(source)
    return ClockedStreamProvider(source, interval=clocked / 1000)


async def main():
    args = parse_arguments()

    frame_queue = asyncio.Queue()

    async with create_input_source(args) as source:
        stream_provider = create_stream_provider(source, args)

        stream_reader = MJPEGStreamReader(stream_provider, frame_queue)
        frame_broker = FrameBroker(frame_queue)
        app = make_app(frame_broker)

        await asyncio.gather(
            run_app(app, args.listen, args.port),
            stream_reader.run(),
            frame_broker.run(),
        )


asyncio.run(main())
