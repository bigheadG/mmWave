# mmWave
mmWave SDK examples based on Batman Kit mmWave Sensor module
This App works with Raspberry Pi 3, Pi 2 and Jetson Nano
Run this repository example needs install mmWave lib.
Those examples are VSD,HAM,PMB examples: 
VSD stands for Vital Signs Detection, HAM stands for High Accuracy Measurement and PMB stands for People Moving Behavior.

# Install Library:
      mmWave Library
      $sudo pip3 install mmWave
      
      tkinter Library
      $sudo pip3 install tkinter
      or
      $sudo apt-get install python3-tk python-tk
      
      numpy Library
      $sudo pip3 install numpy
      or
      $sudo apt-get install python3-numpy python-numpy
      
      pySerial Library
      $sudo pip3 install pySerial
      
      RPi.GPIO library please reference:
      https://www.raspberrypi-spy.co.uk/2012/05/install-rpi-gpio-python-library/

# How to Enable RPi UART port:
Enable UART:

      1:[MainMenu] -> [Preferences] -> [Raspberry Pi Configuration]
         
![MainMenu 0](https://github.com/bigheadG/mmWave/blob/master/UART0.png)

      2:Select [Interface Tab] in Raspberry Pi Configuration
      
      3:Enable Serial Port: Check radio RadioButton
      
![MainMenu 1](https://github.com/bigheadG/mmWave/blob/master/UART1.png)

      4:List tty Device
      
      $ls /dev/tty*
      $sudo chmod +666 /dev/ttyS0
      or 
      $sudo chmod +666 /dev/ttyAMA0
      
      Reboot
![MainMenu 1](https://github.com/bigheadG/mmWave/blob/master/UART3.png)     


# Video Demo(Press ICON to watch the Video)
## Vital Signs Detection:
[![Watch the Video](https://github.com/bigheadG/mmWave/blob/master/heart160.png)](https://youtu.be/4MSrxUmm69M "Watch the Video")
## High Accuracy Measurement:
[![Watch the video](https://github.com/bigheadG/mmWave/blob/master/measure160.png)](https://youtu.be/IEmM7JIqtTc "Watch the Video")
## People Moving Behavior:
[![Watch the video](https://github.com/bigheadG/mmWave/blob/master/people160.png)](https://youtu.be/KuTrT1_m29k "Watch the Video")
