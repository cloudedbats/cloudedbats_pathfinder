#
# Cloudedbats - Pathfinder.
#

import pyaudio

from pathf_core.logger import Logger
from pathf_core.configuration import Configuration
from pathf_core.sound_capture import SoundCapture
from pathf_core.sound_pitchshifting import SoundPitchshifting
from pathf_core.sound_playback import SoundPlayback
from pathf_core.pathf_main import PathfinderMain

# Instances of objects.
audio = pyaudio.PyAudio()
logger = Logger(logger="Pathfinder")
config = Configuration(logger="Pathfinder")
capture = SoundCapture(audio, logger="Pathfinder")
pitchshifting = SoundPitchshifting(logger="Pathfinder")
playback = SoundPlayback(audio, logger="Pathfinder")
pathf_main = PathfinderMain(logger="Pathfinder")
