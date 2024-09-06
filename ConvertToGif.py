__version__ = "1.0"

from meshroom.core import desc


class ConvertToGif(desc.CommandLineNode):
    category = "Video Utils"
    documentation = """This standalone node converts an input video or sequence of images into a GIF with the specified characteristics using FFMPEG."""

    inputs = [
        desc.BoolParam(
            name="inputIsVideo",
            label="Video Input",
            description="Select if the input file is a video instead of a sequence of images.",
            value=False,
            enabled=lambda node: not node.inputIsExr.value
        ),
        desc.BoolParam(
            name="inputIsExr",
            label="EXR Inputs",
            description="Select if the input file is a sequence of EXR images so that the correct conversion flag can be applied.",
            value=False,
            enabled=lambda node: not node.inputIsVideo.value
        ),
        desc.BoolParam(
            name="optimizeCompression",
            label="Optimize Compression",
            description="Select if the conversion to GIF needs to be as compressed as possible. The resulting GIF's size will be smaller, but there might be some impact "
                        "on the final result.",
            value=False,
        ),
        desc.File(
            name="inputFiles",
            label="Input Files",
            description="Input files to convert into a GIF. It can be a video or a list of images, with or without a pattern.",
            value="",
        ),
        desc.StringParam(
            name="outputName",
            label="Output Name",
            description="Filename of the output GIF.",
            value="output.gif",
        ),
        desc.IntParam(
            name="framerate",
            label="Framerate",
            description="Framerate for the output GIF.",
            value=10,
            range=(1, 100, 1),
        ),
        desc.StringParam(
            name="outputSize",
            label="Output Size",
            description="Size of the output GIF, written as \"width:height\" (e.g. 320:200). Setting either width or height to -1 will preserve the aspect ratio.\n"
                        "For no rescale to be applied, set the size to \"-1:-1\".",
            value="320:-1",
        ),
    ]

    outputs = [
        desc.File(
            name="outputGif",
            label="Output GIF",
            description="Generated GIF.",
            value=desc.Node.internalFolder + "{outputNameValue}",
        ),
    ]

    def processChunk(self, chunk):
        if chunk.node.attribute("inputIsVideo").value:
            if chunk.node.attribute("optimizeCompression").value:
                self.commandLine = "ffmpeg -y -i {inputFilesValue} -filter_complex \"fps={framerateValue},scale={outputSizeValue}:flags=lanczos,split[s0][s1];[s0]palettegen=max_colors=32[p];[s1][p]paletteuse=dither=bayer\" {outputGifValue}"
            else:
                self.commandLine = "ffmpeg -y -i {inputFilesValue} -framerate {framerateValue} -vf scale={outputSizeValue} {outputGifValue}"
        else:
            if chunk.node.attribute("inputIsExr").value:
                if chunk.node.attribute("optimizeCompression").value:
                    self.commandLine = "ffmpeg -y -pattern_type glob -apply_trc iec61966_2_1 -i {inputFilesValue} -filter_complex \"fps={framerateValue},scale=320:-1:flags=lanczos,split[s0][s1];[s0]palettegen=max_colors=32[p];[s1][p]paletteuse=dither=bayer\" {outputGifValue}"
                else:
                    self.commandLine = "ffmpeg -y -apply_trc iec61966_2_1 -pattern_type glob -i {inputFilesValue} -framerate {framerateValue} -vf scale={outputSizeValue} {outputGifValue}"
            else:
                if chunk.node.attribute("optimizeCompression").value:
                    self.commandLine = "ffmpeg -y -pattern_type glob -i {inputFilesValue} -filter_complex \"fps={framerateValue},scale=320:-1:flags=lanczos,split[s0][s1];[s0]palettegen=max_colors=32[p];[s1][p]paletteuse=dither=bayer\" {outputGifValue}"
                else:
                    self.commandLine = "ffmpeg -y -pattern_type glob -i {inputFilesValue} -framerate {framerateValue} -vf scale={outputSizeValue} {outputGifValue}"
        desc.CommandLineNode.processChunk(self, chunk)

