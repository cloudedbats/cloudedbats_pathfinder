# CloudedBats - Pathfinder

This is a part of the CloudedBats project: http://cloudedbats.org

## Pathfinder

Pathfinder is a handheld detector for active bat monitoring. 
There is no graphical user interface and it is not possible to save recorded files, at least at the moment.
But if the used sound card supports stereo it will be possible to listen to the sound of bats in real time in stereo, 
to make it easier to locate where the bats are.
Maybe there will be some kind of visualisation of the sound in the future, but main focus is to listen and not to be disturbed by the unit.

Image: TODO.

### Design goal

The design goal for the PathFinder is to make it reliable and as simple as possible to operate. 
Just add power to start the Pathfinder and connect your headphones. Remove power for shutdown. 
Some configurations can be done during installation, but not in the field.

### Listen to bats

The ultrasound emitted by bats is converted into audible sound using a technique called pitch shifting.
That means that the time is in real time, but the frequency is divided by a factor of 30 as default. 
In this case a bat sound at 30 kHz will then be translated to 1 kHz.

### Hardware setup

- Ultrasonic microphone with USB connection, 
or stereo sound card/microphones that can run at a sample rater at least 192 kHz.
- Raspberry Pi microcomputer.
- Micro-SD card for the CloudedBats-Pathfinder software.
- PowerBank for mobile use. 

### Installation:

Follow the instructions for CloudedBats_WURB.

Replace the git clone row:

    git clone https://github.com/cloudedbats/cloudedbats_pathfinder.git

Use the "" script to write protected the SD card to avoid problems with the abrupt power off.

TODO: More detailed instruction...

## Contact

Arnold Andreasson, Sweden.

info@cloudedbats.org
