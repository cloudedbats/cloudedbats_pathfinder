# 
# Cloudedbats - Pathfinder.
#

from pathfinder.pathf_logging import PathfinderLogger
from pathfinder.pathf_config import PathfinderConfig
from pathfinder.sound_cards import SoundCards
from pathfinder.sound_capture import SoundCapture
from pathfinder.sound_pitchshifting import SoundPitchshifting
from pathfinder.sound_playback import SoundPlayback

from pathfinder.pathf_main import main

# To be used similar to singleton objects.

logger = PathfinderLogger(logger="Pathfinder")
config = PathfinderConfig(logger="Pathfinder")
sound_cards = SoundCards(logger="Pathfinder")
sound_capture = SoundCapture(logger="Pathfinder")
sound_pitchshifting = SoundPitchshifting(logger="Pathfinder")
sound_playback = SoundPlayback(logger="Pathfinder")
