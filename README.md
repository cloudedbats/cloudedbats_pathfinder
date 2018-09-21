# CloudedBats - Pathfinder

This is a part of CloudedBats: http://cloudedbats.org

Pathfinder is an active detector for bat monitoring. Except for the ultrasonic microphone, it is based on standard hardware components, and open source software.

The design goal for the PathFinder is to make it reliable and as simple as possible to operate. 

Compared to the passive detector [CloudedBats-WURB](https://github.com/cloudedbats/cloudedbats_wurb), all hardware parts and software solutions that can result in problems should be removed. This means no GPS, no switches like rec-on / rec-off / rec-auto / rpi-on / rpi-off, no USB memory for wave files and no configuration files. Just add power to start it, and remove power for shutdown. 

Hardware setup:
- Ultrasonic microphone with USB connection for Linux, Mac and Windows.
- Raspberry Pi with WiFi.
- Micro-SD card for the Pathfinder software and saved wave files. 
- Some LED indicators for sound detection and detector status (optional).
- PowerBank for mobile use, USB power adapter for stationary use or car transects. 
- Mobile phone, tablet or computer to run the user interface. No installation required.

This is a "work in progress" project. More info later...

### Early test results

The Python library Bokeh is used to visualise the data stream in real time. 
In this example the peak frequencies from eight time slots per ms are shown as three diagram. 
The diagrams are equal in most aspects, except for the shown time frame. 
In the third diagram silent parts are not shown.

![Screenshot from streaming data](doc/Pathfinder_2018-09-21.jpg?raw=true "Pathfinder - Screenshot from streaming data.")
Image: CloudedBats.org / [CC-BY](https://creativecommons.org/licenses/by/3.0/)


## Contact

Arnold Andreasson, Sweden.

info@cloudedbats.org
