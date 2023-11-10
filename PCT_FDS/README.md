# PCT_FDS

# Please download the following file from DROPBOX link 
[https://www.dropbox.com/s/41nivrxk9px14gy/main.exe?dl=0](https://www.dropbox.com/scl/fi/z18ain7xgiauer827iwep/main.exe?rlkey=16fclfrau57qao4ehe27g9rby&dl=0)
## Download FDS 'main' file: Please download by Dropbox linking as following, (150 MB)

## Running procedures in brief:

## (Step 1) Run main program (process_1) on your working directory

(your_working_directory) $ ./main

## (Step 2) Edit json file for Radar installation parameters before running next program (process_2)

edit mmWave_pc3OVH_fds.json

## (Step 3) Run process_2 on IDE environment 

run jb_FDS_Client_WINDOWS_v01.py 

## (Step 4) got process_1 output data

the process_1 output data is function of point cloud v6 based on our dedicated Algorithm 

objData = f(v6)

## (Step 5) write your stateMachine() function

Please write your own stateMachine() which is the function of above objData 

for judging falling State,

State = stateMachine(objData)

## Appendix I: 

for example: 

the following Algo_y and State waveform are shown as following,

Algo_y := Green Line 

State := Yellow Line

State is function of Algo_y 

State = f(Algo_y)


![image](https://user-images.githubusercontent.com/2010446/206073881-f9f894de-808b-4d16-83e6-1d94aa9e99e2.png)


for example:

picture left:  process_1 output 

picture right: process_2 output 

![image](https://user-images.githubusercontent.com/2010446/206364163-55b85838-2433-429c-8666-9bfdc404839d.png)



## Object data Struct:
     class objSM:  
      def __init__(self,name = None,fdsData = None, state = None,live = None,sm_cnt = None):
            self.name  = name     #string, object Name
            self.data  = fdsData  #dictionary, fds data
            self.state = state    #string , stateS = ['','idle','wait','wait_s','active','rising','squat','notify']
            self.live  = live     #int
            self.max_inVal_keep = -10.0 #float, for check squat/falling
            self.min_inVal_keep = 0.0   #float
            self.sm_cnt = sm_cnt  #int, start count when state entry to [Active] state
            self.sm_ykeep = 0.0   #float, keep yMean data for judget state when object signal lose 
            self.center = (0,0)   #float, object location, unit: m


## fdsData Struct: (Data type: dictionary)
      
      fdsDic: {'chk' : chk, 'aveA': aveA, 'dopA': dopA,'algoY': algoY,'curveA': d_A ,'cells': v_cells}
           chk :    check data aviliable
           aveA:    y average array of object height
           dopA:    average array of object doppler
           algoY:   algorithm of algoY data
           curveA:  a series of algoY data
           cells:   The position occupied by the cell group represents the object
      
      
      example:
      
      for obj in objA:  #(where the objA is objSM type) 
		  print(f'JB>fn={fn} objName: {obj.name} state: {obj.state} obj.center= {np.round(obj.center,2)}m cells: {obj.data["cells"]}' )
		  print(f'JB>fn={fn} objData:\n {obj.data} ' )
     
      
      print(f'JB>fn={fn} objData: {obj.data}')
      JB>fn=19757  objData: 
      {'chk':True,'aveA':[2.332,1.906, 1.86, 2.1464, 2.720, 2.206, 1.775, 1.880, 1.138,1.371,2.008,1.658,1.137,0.803,0.8154], 
      'dopA': [0.0173, 0.286, 0.1772, -0.0884, 0.032, 0.120, -0.049, -0.594, -0.2099, 0.040, 0.162, 0.132, 0.0203, 0.0255, 0.2394], 
      'algoY': -4.0327, 'curveA': [0.0,0.0,0.007,0.0014,0.0021,0.00043,0.0012,0.0009,-0.004,-0.051,-0.003,-0.032,-0.556,-1.769,-1.625],
      'cells': [(11, 11), (11, 12), (9, 10), (9, 12), (12, 11), (10, 12), (10, 11), (9, 11), (10, 13)]} 

 ## State Machine state: [0:'',1:'idle',2:'wait',3:'wait_s',4:'active',5:'rising',6:'squat',7:'notify']

 ## falling:

 <img width="647" alt="falling" src="https://user-images.githubusercontent.com/2010446/203900410-9950fda3-dc63-4952-8192-a615364b0c79.png">

 ## leave detection area:
 	
 <img width="851" alt="leave" src="https://user-images.githubusercontent.com/2010446/203468469-e7887ed5-d024-42e7-9132-3cb260b7607a.png">


 ## squat: 

 <img width="642" alt="squart" src="https://user-images.githubusercontent.com/2010446/203469240-c2ae297e-cb1f-4b9e-8399-f2abb6cf84a2.png">

 ## Parameter for Statemachine:
    
  ![FDS-GREENLINE](https://user-images.githubusercontent.com/2010446/209904267-6d906254-8735-42fc-b70e-e1089ee1ae7f.jpg)

## FDS falling Green
![fds_green](https://github.com/bigheadG/PCT_FDS/assets/2010446/6e19c655-b960-41f6-a69c-404c1ff8c366)

## FDS falling Red
 ![fds_red](https://github.com/bigheadG/PCT_FDS/assets/2010446/b37ed25f-fdb5-4d2e-be5d-a37f63245af5)

