# mmWave-HAM (High Accuracy Measurement)
This repository contains the Batman Kit- HAM mmWave Sensor SDK. 



 
The High Accuracy Measurement (HAM) based Batman Kit is for measuring object distance 
from the mmWave Sensor Module with the range of 30cm ~ 3meters(about 1~10 feet) with millimeter resolution.


## Installing
 (1) Hardware:
     - Connect mmWave Batman-BT101 to Arduino DUE
     - Coonect 6 MATRIX LEDs 
     See Drawing for more detail
 
 (2) Firmware:
     - Download program codes of draft.ino
      
      
 # Notes: 
   1. connection MMWAVE TX1 => DUE RX1
      on {MMWAVE GPIO_0 LOW} select KEY data(115200) else RAW data(921600)   


# reference:

1. LabGuide: https://github.com/bigheadG/mmWaveDocs/blob/master/high_accuracy_16xx_lab_user_guide.pdf

          (Alert: if DATA STARUCTURE could not be found in PDF please see above Data Structure of README.md instead)

2. KeyDataProtocol: https://github.com/bigheadG/mmWaveDocs/blob/master/V2_highAccuracyBLEProtocol_v02_02_pdf.pdf
