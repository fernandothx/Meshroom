__version__ = "1.1"

from meshroom.core import desc, stats


class FeatureExtraction(desc.CommandLineNode):
    commandLine = 'aliceVision_featureExtraction {allParams}'
    size = desc.DynamicNodeSize('input')
    parallelization = desc.Parallelization(blockSize=40)
    commandLineRange = '--rangeStart {rangeStart} --rangeSize {rangeBlockSize}'

    inputs = [
        desc.File(
            name='input',
            label='Input',
            description='SfMData file.',
            value='',
            uid=[0],
        ),
        desc.ChoiceParam(
            name='describerTypes',
            label='Describer Types',
            description='Describer types used to describe an image.',
            value=['sift'],
            values=['sift', 'sift_float', 'sift_upright', 'akaze', 'akaze_liop', 'akaze_mldb', 'cctag3', 'cctag4', 'sift_ocv', 'akaze_ocv'],
            timeFactor=[-1, 0, 0, 4, 0, 0, 0, 0, 0, 0],
            exclusive=False,
            uid=[0],
            joinChar=',',
        ),
        desc.ChoiceParam(
            name='describerPreset',
            label='Describer Preset',
            description='Control the ImageDescriber configuration (low, medium, normal, high, ultra). Configuration "ultra" can take long time !',
            value='normal',
            values=['low', 'medium', 'normal', 'high', 'ultra'],
            timeFactor=[0.1, 0.25, 1, 1.1, 5.25],
            exclusive=True,
            uid=[0],
        ),
        desc.BoolParam(
            name='forceCpuExtraction',
            label='Force CPU Extraction',
            description='Use only CPU feature extraction.',
            value=True,
            uid=[],
            advanced=True,
        ),
        desc.IntParam(
            name='maxThreads',
            label='Max Nb Threads',
            description='Specifies the maximum number of threads to run simultaneously (0 for automatic mode).',
            value=0,
            range=(0, 24, 1),
            uid=[],
            advanced=True,
        ),
        desc.ChoiceParam(
            name='verboseLevel',
            label='Verbose Level',
            description='verbosity level (fatal, error, warning, info, debug, trace).',
            value='info',
            values=['fatal', 'error', 'warning', 'info', 'debug', 'trace'],
            exclusive=True,
            uid=[],
        )
    ]

    outputs = [
        desc.File(
            name='output',
            label='Output Folder',
            description='Output path for the features and descriptors files (*.feat, *.desc).',
            value=desc.Node.internalFolder,
            uid=[],
        ),
    ]

    def getEstimatedTime(self, chunk, reconstruction):
        factor = 1.216368273112215e-05 # Calculated by (time taken / number of images) / (benchmark * image resolution x * image resolution y)
        amount, pixels = reconstruction.imagesStatisticsForNode(chunk.node)
        return chunk.node.getTotalTime(factor*stats.Benchmark()*pixels*amount)
