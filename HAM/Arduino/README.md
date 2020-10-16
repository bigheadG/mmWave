## mmWave TMD Arduino (Released on 2020.10.16)

This repository contains the Batman Kit- HAM mmWave Sensor SDK. 
The High Accuracy Measurement (HAM) based Batman Kit is for measuring object distance 
from the mmWave Sensor Module with the range of 0.3 ~ 3.0 meters(about 1 ~ 10 feet) with millimeter accuracy.

# Installing:
 (1) Hardware:
     
     - Connect mmWave Batman-BT101 to Arduino DUE Board
     
     - Connect to WS2812B LED STRIP
 
     - Connection chain as following, 
       mmWave module => Arduino DUE board => WS2812B LED Strip
 
 (2) Firmware:
 
     - Download program codes of "jb_VI809_highAccuracy_onDue_released.ino"
     
     - One library of "FastLED V3.3.2" should be installed before compilation
     
     - Based on Arduino IDE V1.8.10 (or later version)
      
# Notes: 
   1. The mmWave jumper should be selected for "KEY Data Mode" with baud rate 115200/8/n/1 
   

# Reference:

1. LabGuide: https://github.com/bigheadG/mmWaveDocs/blob/master/high_accuracy_16xx_lab_user_guide.pdf

          (Alert: if DATA STARUCTURE could not be found in PDF please see above Data Structure of README.md instead)

2. KeyDataProtocol: https://github.com/bigheadG/mmWaveDocs/blob/master/V2_highAccuracyBLEProtocol_v02_02_pdf.pdf

