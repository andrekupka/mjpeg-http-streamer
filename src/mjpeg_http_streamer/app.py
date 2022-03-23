from aiohttp import web

FRAME_BROKER_KEY = 'frame_broker'


async def get_snapshot(request):
    frame_broker = request.app[FRAME_BROKER_KEY]
    frame = frame_broker.current_frame
    if frame is None:
        return web.Response(text="no snapshot", status=404)

    return web.Response(body=frame, content_type='image/jpeg')


async def get_stream(request):
    frame_broker = request.app[FRAME_BROKER_KEY]
    with frame_broker.subscribe() as subscription:
        boundary = 'foobar'

        stream = web.StreamResponse(
            status=200,
            reason='OK',
            headers={
                'Content-Type': f'multipart/x-mixed-replace;boundary={boundary}'
            }
        )

        await stream.prepare(request)

        header = f'--{boundary}\r\nContent-Type: image/jpeg\r\n'.encode()

        async def write_frame(source_frame, prefix=b'\r\n'):
            message = prefix + header + f'Content-Length: {len(source_frame)}\r\n\r\n'.encode() + source_frame
            await stream.write(message)

        await write_frame(frame_broker.current_frame, prefix=b'')

        while True:
            frame = await subscription.get()
            if frame is None:
                break

            await write_frame(frame)

        await stream.write_eof()
        return stream


def make_app(frame_broker):
    app = web.Application()
    app[FRAME_BROKER_KEY] = frame_broker
    app.add_routes([
        web.get('/snapshot', get_snapshot),
        web.get('/stream', get_stream)
    ])

    return app


async def run_app(app, listen_host, port):
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, host=listen_host, port=port)
    await site.start()
