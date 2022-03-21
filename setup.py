from setuptools import setup

# Metadata goes in setup.cfg. These are here for GitHub's dependency graph.
setup(
    name='mjpeg_http_streamer',
    install_requires=[
        'aiohttp >= 3.8'
    ]
)
