# mmWave-HAM (High Accuracy Measurement)
This repository contains the Batman Kit- HAM mmWave Sensor SDK. 
The sample code below consists of instruction for using the mmWave lib.
This mmWave-HAM Python Program will work with High Accuracy Measurement (HAM) based mmWave Batman Kit solution.
This App works with Raspberry Pi 3 , Pi 2 and Jetson Nano
The High Accuracy Measurement (HAM) based Batman Kit is for measuring object distance 
from the mmWave Sensor Module with the range of 30cm ~ 3meters(about 1~10 feet) 
with millimeter resolution.


## Installing
//* V02.01 2020.03.18 1. cloned from V22.04 for HAM project
//*                   2. show 6 LEDs
//*                   3. Data:   connection MMWAVE TX1 => DUE RX1 , on {MMWAVE GPIO_0 LOW} select KEY data(115200) else RAW data(921600)   
//*                   4. Config: connection DUE TX2 => MMWAVE RX0, sent CONFIG commands (115200)
//* V02.02 2020.03.18 1. build jb_ledWrite6Leds(jb_valueU32), ALERT: pay attention on type as U32
//* V02.03 2020.03.19 1. set moving average per 1 sec 
 
# reference:

1. LabGuide: https://github.com/bigheadG/mmWaveDocs/blob/master/high_accuracy_16xx_lab_user_guide.pdf

          (Alert: if DATA STARUCTURE could not be found in PDF please see above Data Structure of README.md instead)

2. KeyDataProtocol: https://github.com/bigheadG/mmWaveDocs/blob/master/V2_highAccuracyBLEProtocol_v02_02_pdf.pdf
