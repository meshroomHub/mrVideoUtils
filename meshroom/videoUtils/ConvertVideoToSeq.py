__version__ = "1.0"

import os
import logging
from pathlib import Path
from meshroom.core import desc


class ConvertVideoToSeq(desc.CommandLineNode):
    commandLine = "ffmpeg -y -i {videoFileValue}"
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
            value=lambda attr: os.path.join("{nodeCacheFolder}", "frames"),
        ),
    ]

    def processChunk(self, chunk):
        if not os.path.exists(chunk.node.videoFile.value):
            logging.warning('Input video file does not exist: "{}"'.format(chunk.node.videoFile.value))
            return
        folder = chunk.node.outputFolder.value
        logging.warning('Convert video to seq folder: {}'.format(folder))
        if not os.path.exists(folder):
            os.makedirs(folder)
        desc.CommandLineNode.processChunk(self, chunk)

    def buildCommandLine(self, chunk):
        outputFolder = Path(chunk.node.attribute("outputFolder").value)
        filePattern = chunk.node.attribute("pattern").value

        suffix = f" {os.path.join(outputFolder,filePattern)}"
        return desc.CommandLineNode.buildCommandLine(self, chunk) + suffix
