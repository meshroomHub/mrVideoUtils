__version__ = "1.0"

from meshroom.core import desc
from meshroom.core.utils import VERBOSE_LEVEL

class GenerateVideo(desc.CommandLineNode):
    category = "Video Utils"
    documentation = """ Generate a video from a sfmData ordered by frameId """

    inputs = [
        desc.File(
            name="input",
            label="Input",
            description="SfmData used to get the list of images.",
            value="",
        ),
        desc.FloatParam(
            name="framerate",
            label="Camera Frame Rate",
            description="Define the camera's Frames per second.",
            value=24.0,
            range=(1.0, 60.0, 1.0),
        ),
        desc.ChoiceParam(
            name="verboseLevel",
            label="Verbose Level",
            description="Verbosity level (fatal, error, warning, info, debug, trace).",
            values=VERBOSE_LEVEL,
            value="info",
        )
    ]

    outputs = [
        desc.File(
            name='directory',
            label='Intermediate directory',
            description="Intermediate directory",
            value="{nodeCacheFolder}",
        ),
        desc.File(
            name='outputVideo',
            label='Output Video',
            description="Generated video.",
            value="{nodeCacheFolder}/output.mp4",
        )
    ]

    def processChunk(self, chunk):
        
        from pathlib import Path

        import logging
        logging.getLogger().setLevel(chunk.node.verboseLevel.value.upper())
        
        from pyalicevision import sfmDataIO as avsfmdataio
        from pyalicevision import sfmData as avsfmdata

        logging.info("Open input file")
        data = avsfmdata.SfMData()
        ret = avsfmdataio.load(data, chunk.node.input.value, avsfmdataio.VIEWS)
        if not ret:
            logging.error("Cannot open input")
            raise RuntimeError()
        
        # store all image path in sfmData indexed by frame id
        views = data.getViews()
        viewsPerFrameId = {}
        for viewId in views:
            view = views[viewId]
            frameId = view.getFrameId()
            viewsPerFrameId[frameId] = view.getImage().getImagePath()
            

        # sort path per frameId
        viewsPerFrameId = dict(sorted(viewsPerFrameId.items()))
        # Check intermediate directory
        intermediate_directory = Path(chunk.node.directory.value)
        if not (intermediate_directory.exists() and intermediate_directory.is_dir()):
            logging.error("Intermediate directory is not valid")
            raise RuntimeError()

        pos = 0
        suffix = ""
        for frameId, path in viewsPerFrameId.items():
            target = Path(path)
            if suffix == "":
                suffix = target.suffix
            if target.suffix.lower() != suffix.lower():
                logging.error("Multiple image types found.")
                raise RuntimeError()
            
            # Create a link using a sequential order
            link = intermediate_directory / f"{pos:012d}{suffix}"

            # Force symlink creation
            if link.exists() or link.is_symlink():
                link.unlink()

            # Create symbolic link
            link.symlink_to(target)
            pos = pos + 1
        
        self.commandLine = f"ffmpeg -y -framerate {chunk.node.framerate.value} -start_number 0 -i %012d{suffix}  -vf \"scale=trunc(iw/2)*2:trunc(ih/2)*2\" -c:v libx264 -pix_fmt yuv420p {chunk.node.outputVideo.value}"
        desc.CommandLineNode.processChunk(self, chunk)