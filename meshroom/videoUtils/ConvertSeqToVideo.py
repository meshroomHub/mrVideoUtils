__version__ = "1.0"

import os
from meshroom.core import desc


class ConvertSeqToVideo(desc.CommandLineNode):
    # use scale to avoid not even width or height ffmpeg error
    commandLine = 'ffmpeg -y -framerate {framerateValue} -pattern_type glob -i {imagesValue}  -vf "scale=trunc(iw/2)*2:trunc(ih/2)*2" {outputVideoValue} '
    gpu = desc.Level.NONE

    category = "Video Utils"
    documentation = """
Create a video from images.
"""

    inputs = [
        desc.File(
            name="images",
            label="Images",
            description="List of the images.",
            value="",
        ),
        desc.FloatParam(
            name="framerate",
            label="Framerate",
            description="Video framerate.",
            value=24.0,
            range=(10.0, 120.0, 1.0),
        ),
    ]

    outputs = [
        desc.File(
            name="outputVideo",
            label="Output Video",
            description="Output video file.",
            value="{nodeCacheFolder}/video.mp4",
        ),
    ]
