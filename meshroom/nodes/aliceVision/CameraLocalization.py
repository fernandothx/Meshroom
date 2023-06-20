__version__ = "1.0"

import os
from meshroom.core import desc


class CameraLocalization(desc.AVCommandLineNode):
    commandLine = 'aliceVision_cameraLocalization {allParams}'

    category = 'Utils'
    documentation = '''
    '''

    inputs = [
        desc.File(
            name="sfmdata",
            label="SfMData",
            description="The SfMData file generated by AliceVision.",
            value="",
            uid=[0],
        ),
        desc.File(
            name="mediafile",
            label="Media File",
            description="The folder path or the filename for the media to track.",
            value="",
            uid=[0],
        ),
        desc.File(
            name="visualDebug",
            label="Visual Debug Folder",
            description="If a folder is provided, this enables visual debug and all the debugging information will be saved in that folder.",
            value="",
            uid=[0],
        ),
        desc.File(
            name="descriptorPath",
            label="Descriptor Path",
            description="Folder containing the descriptors for all the images (ie. the *.desc.).",
            value="",
            uid=[0],
        ),
        desc.ChoiceParam(
            name="matchDescTypes",
            label="Match Desc Types",
            description="Describer types to use for the matching.",
            value=["dspsift"],
            values=["sift", "sift_float", "sift_upright", "dspsift", "akaze", "akaze_liop", "akaze_mldb", "cctag3", "cctag4", "sift_ocv", "akaze_ocv"],
            exclusive=False,
            uid=[0],
            joinChar=",",
        ),
        desc.ChoiceParam(
            name="preset",
            label="Preset",
            description="Preset for the feature extractor when localizing a new image (low, medium, normal, high, ultra).",
            value="normal",
            values=["low", "medium", "normal", "high", "ultra"],
            exclusive=True,
            uid=[0],
        ),
        desc.ChoiceParam(
            name="resectionEstimator",
            label="Resection Estimator",
            description="The type of *sac framework to use for resection (acransac, loransac).",
            value="acransac",
            values=["acransac", "loransac"],
            exclusive=True,
            uid=[0],
        ),
        desc.ChoiceParam(
            name="matchingEstimator",
            label="Matching Estimator",
            description="The type of *sac framework to use for matching (acransac, loransac).",
            value="acransac",
            values=["acransac", "loransac"],
            exclusive=True,
            uid=[0],
        ),
        desc.File(
            name="calibration",
            label="Calibration",
            description="Calibration file.",
            value="",
            uid=[0],
        ),
        desc.BoolParam(
            name="refineIntrinsics",
            label="Refine Intrinsics",
            description="Enable/Disable camera intrinsics refinement for each localized image.",
            value=False,
            uid=[0],
        ),
        desc.FloatParam(
            name="reprojectionError",
            label="Reprojection Error",
            description="Maximum reprojection error (in pixels) allowed for resectioning. If set to 0, it lets the ACRansac select an optimal value.",
            value=4.0,
            range=(0.1, 50.0, 0.1),
            uid=[0],
        ),
        desc.IntParam(
            name="nbImageMatch",
            label="Nb Image Match",
            description="[voctree] Number of images to retrieve in database.",
            value=4,
            range=(1, 1000, 1),
            uid=[0],
        ),
        desc.IntParam(
            name="maxResults",
            label="Max Results",
            description="[voctree] For algorithm AllResults, it stops the image matching when this number of matched images is reached. If 0 it is ignored.",
            value=10,
            range=(1, 100, 1),
            uid=[0],
        ),
        desc.IntParam(
            name="commonviews",
            label="Common Views",
            description="[voctree] Number of minimum images in which a point must be seen to be used in cluster tracking.",
            value=3,
            range=(2, 50, 1),
            uid=[0],
        ),
        desc.File(
            name="voctree",
            label="Voctree",
            description="[voctree] Filename for the vocabulary tree.",
            value="${ALICEVISION_VOCTREE}",
            uid=[0],
        ),
        desc.File(
            name="voctreeWeights",
            label="Voctree Weights",
            description="[voctree] Filename for the vocabulary tree weights.",
            value="",
            uid=[0],
        ),
        desc.ChoiceParam(
            name="algorithm",
            label="Algorithm",
            description="[voctree] Algorithm type: FirstBest, AllResults.",
            value="AllResults",
            values=["FirstBest", "AllResults"],
            exclusive=True,
            uid=[0],
        ),
        desc.FloatParam(
            name="matchingError",
            label="Matching Error",
            description="[voctree] Maximum matching error (in pixels) allowed for image matching with geometric verification. If set to 0, it lets the ACRansac select an optimal value.",
            value=4.0,
            range=(0.0, 50.0, 1.0),
            uid=[0],
        ),
        desc.IntParam(
            name="nbFrameBufferMatching",
            label="Nb Frame Buffer Matching",
            description="[voctree] Number of previous frames of the sequence to use for matching (0 = Disable).",
            value=10,
            range=(0, 100, 1),
            uid=[0],
        ),
        desc.BoolParam(
            name="robustMatching",
            label="Robust Matching",
            description="[voctree] Enable/Disable the robust matching between query and database images, all putative matches will be considered.",
            value=True,
            uid=[0],
        ),
        desc.IntParam(
            name="nNearestKeyFrames",
            label="N Nearest Key Frames",
            description="[cctag] Number of images to retrieve in the database. Parameters specific for final (optional) bundle adjustment optimization of the sequence.",
            value=5,
            range=(1, 100, 1),
            uid=[0],
        ),
        desc.StringParam(
            name="globalBundle",
            label="Global Bundle",
            description="[bundle adjustment] If --refineIntrinsics is not set, this option allows to run a final global bundle adjustment to refine the scene.",
            value="",
            uid=[0],
        ),
        desc.BoolParam(
            name="noDistortion",
            label="No Distortion",
            description="[bundle adjustment] It does not take into account distortion during the BA, it considers the distortion coefficients to all be equal to 0.",
            value=False,
            uid=[0],
        ),
        desc.BoolParam(
            name="noBArefineIntrinsics",
            label="No BA Refine Intrinsics",
            description="[bundle adjustment] If set to true, does not refine intrinsics during BA.",
            value=False,
            uid=[0],
        ),
        desc.IntParam(
            name="minPointVisibility",
            label="Min Point Visibility",
            description="[bundle adjustment] Minimum number of observations that a point must have in order to be considered for bundle adjustment.",
            value=2,
            range=(2, 50, 1),
            uid=[0],
        ),
        desc.ChoiceParam(
            name="verboseLevel",
            label="Verbose Level",
            description="Verbosity level (fatal, error, warning, info, debug, trace).",
            value="info",
            values=["fatal", "error", "warning", "info", "debug", "trace"],
            exclusive=True,
            uid=[],
        ),
    ]

    outputs = [
        desc.File(
            name="outputAlembic",
            label="Alembic",
            description="Filename for the SfMData export file (where camera poses will be stored).",
            value=desc.Node.internalFolder + "trackedCameras.abc",
            uid=[],
        ),
        desc.File(
            name="outputJSON",
            label="JSON File",
            description="Filename for the localization results as .json.",
            value=desc.Node.internalFolder + "trackedCameras.json",
            uid=[],
        ),
    ]

