# CloudedBats - Pathfinder

This is a part of the CloudedBats project: http://cloudedbats.org

Note: This is a "work in progress" project running on a spare time basis. Contact info below if you want to join me...

## Pathfinder

Pathfinder is a handheld detector for bat monitoring. Except for the ultrasonic microphone, it is based on standard hardware components, and open source software. Instead of an integrated display the unit will act as a WiFi hotspot and any device with WiFi and a web browser can be connected to it. 

The design goal for the PathFinder is to make it reliable and as simple as possible to operate. 

Compared to the passive detector [CloudedBats-WURB](https://github.com/cloudedbats/cloudedbats_wurb), all hardware parts and software solutions that can result in problems should be removed. This means no GPS, no switches like rec-on / rec-off / rec-auto / rpi-on / rpi-off and no configuration files. USB memory for wave files will be optional and should not breake the basic functionality if it fails in some way. Just add power to start it, and remove power for shutdown. 

Hardware setup:
- Ultrasonic microphone with USB connection for Linux, Mac and Windows.
- Raspberry Pi with WiFi.
- Micro-SD card for the CloudeBats-Pathfinder software. This will be write protected to avoid problems with lost of power.
- USB memory for saved wave files (optional). 
- Some LED indicators for sound detection and detector status (optional).
- PowerBank for mobile use, USB power adapter for stationary use or car transects. 
- Mobile phone, tablet or computer to run the user interface. No installation required.

### Early test results (2018-09-22)

The Python library Bokeh is used to visualise the data stream in real time. 
In this example the peak frequencies from eight time slots per ms are shown as three diagram. 
The diagrams are equal in most aspects, except for the shown time frames. 
In the third diagram silent parts are hidden.

Note: This is not based on Zero Crossing, it's only interpolated peak values from real time FFT. But I really like many parts from ZC, for example the compact format and the focus on call shapes. Why should users even bother about stuff like "window size" and  "windowing functions" (Hamming, Blackman-Harris, etc.), software should handle that automatically... 

Screenshot:
![Screenshot from streaming data](doc/Pathfinder_2018-09-21.jpeg?raw=true "Pathfinder - Screenshot from streaming data.")
Image: CloudedBats.org / [CC-BY](https://creativecommons.org/licenses/by/3.0/)

#### For developers:

Code for the test can be found here: 
[pathfinder_single_user_flask](/pathfinder_single_user_flask)
 
The example is using the micro web framework Flask and a test wave file is included. Run pathfinder_flask.py and connect from a web browser at address "localhost:5000".


## Contact

Arnold Andreasson, Sweden.

info@cloudedbats.org
