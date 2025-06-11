__version__ = "1.0"

import os
import logging
from pathlib import Path
from meshroom.core import desc


class ConvertVideoToSeq(desc.CommandLineNode):
    commandLine = "ffmpeg -y -i {videoFileValue} {outputFolderValue}/{patternValue}"
    gpu = desc.Level.NONE

    category = "Video Utils"
    documentation = """
Extract frames from a video.
"""

    inputs = [
        desc.File(
            name="videoFile",
            label="Video File",
            description="Video file to extract the frames from.",
            value="",
        ),
        desc.StringParam(
            name="pattern",
            label="Output Sequence Pattern",
            description="Filename pattern for the output frames.",
            value="frame_%04d.png",
        ),
    ]

    outputs=[
        desc.File(
            name="outputFolder",
            label="Output Folder",
            description="Folder where to save the frames.",
            value="{nodeCacheFolder}/frames",
        ),
        desc.File(
            name="outputSequence",
            label="Output Sequence",
            description="Output image sequence.",
            value="{nodeCacheFolder}/frames/*",
            semantic="sequence",
            group="",
        ),
    ]

    def processChunk(self, chunk):
        folder = chunk.node.outputFolder.value
        logging.warning('Convert video to seq folder: {}'.format(folder))
        if not os.path.exists(folder):
            os.makedirs(folder)
        desc.CommandLineNode.processChunk(self, chunk)
