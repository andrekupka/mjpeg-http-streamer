import argparse


SOURCE_STDIN = "stdin"
SOURCE_FIFO = "fifo"


def port(value):
    int_value = int(value)
    if int_value < 1 or int_value > 65535:
        raise ValueError('Port must be in range [1:65535].')
    return int_value


def positive_int(value):
    int_value = int(value)
    if int_value < 1:
        raise ValueError('Value must be a positive integer.')
    return int_value


def parse_arguments():
    parser = argparse.ArgumentParser(
        prog='mjpeg_http_streamer',
        description='Create an mjpeg http stream from different sources.'
    )

    parser.add_argument('-l', '--listen', type=str, default='localhost',
                        help='The host/ip to create the http server on.')
    parser.add_argument('-p', '--port', type=port, default=8080,
                        help='The port for the http server to listen on.')

    parser.add_argument('-c', '--clocked',
                        help="""
                        By default frames from the mjpeg stream are read as fast as possible. With -c/--clocked set, the
                        given amount of time in milliseconds is slept between frames.
                        """,
                        type=positive_int)

    parser.add_argument("-s", "--source", type=str, choices=[SOURCE_STDIN, SOURCE_FIFO], default=SOURCE_STDIN,
                        help='Specifies the mjpeg input source.')

    return parser.parse_args()
