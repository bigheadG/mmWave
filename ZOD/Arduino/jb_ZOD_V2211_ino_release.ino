//***********************************************************************************************************                  
//* jb_ZOD_V2211_ino_release.ino based on Arduino 1.8.10
//* ALERT: 1. Zone1 and Zone2 area are defined on mmWave ZOD firmware
//*           those values may be changed by application
//*        2. JBL_targetZoneStateU16 value is defined by mmWave ZOD firmeware 
//***********************************************************************************************************                  
#define JB_2211 2211
#define JB_PROJECT_VERSION "V22.11_ino_release"
#define JB_PROJECT_NAME  "\n\nJB> jb_ZOD_" JB_PROJECT_VERSION "\n"
//***********************************************************************************************************                  
//* define JB parameters
#define JB_TABLE_WIDTH_8                  8 
#define JB_NUMBER_OF_LEDS_4               4
#define JB_CLOCK_PIN_5                    5
#define JB_DATA_LATCH_PIN_6               6 
#define JB_DATA_PIN_7                     7 
//* define MAX7219 parameters
#define MAX7219_DECODE_REGISTER           (0x09)
#define MAX7219_INTENSITY_REGISTER        (0x0A)
#define MAX7219_SCANLIMIT_REGISTER        (0x0B)  
#define MAX7219_SHUTDOWN_REGISTER         (0X0C)
#define MAX7219_DISPLAYTEST_REGISTER      (0x0F)
#define MAX7219_COLUMN_REGISTER(col)      ((col) + 1)
#define MAX7219_NOOP_REGITER              (0x00)
#define MAX7219_OFF_0x00                  (0x00)
#define MAX7219_ON_0x01                   (0x01)
//***********************************************************************************************************                  

//***********************************************************************************************************                  
//* define JB LED TABLE[13][8], 0..9 and ARROW icon
#define JB_ICON_BLACK     10
#define JB_ICON_UP        11
#define JB_ICON_DOWN      12
#define JB_TABLE_DEPTH_13 13
#define JB_TABLE_WIDTH_8  8
const uint8_t JB_LED_TABLE_8x8[JB_TABLE_DEPTH_13][JB_TABLE_WIDTH_8] = {               
  {0x00,0x38,0x44,0x44,0x44,0x44,0x44,0x38}, // (22.11) 0                     
  {0x00,0x10,0x30,0x50,0x10,0x10,0x10,0x7c}, // (22.11) 1
  {0x00,0x38,0x44,0x04,0x18,0x20,0x40,0x7c}, // (22.11) 2
  {0x00,0x38,0x44,0x04,0x18,0x04,0x44,0x38}, // (22.11) 3
  {0x00,0x08,0x18,0x28,0x48,0x7c,0x08,0x08}, // (22.11) 4
  {0x00,0x7c,0x40,0x40,0x78,0x04,0x04,0x78}, // (22.11) 5
  {0x00,0x3c,0x40,0x40,0x78,0x44,0x44,0x38}, // (22.11) 6
  {0x00,0x7c,0x04,0x04,0x08,0x10,0x20,0x40}, // (22.11) 7
  {0x00,0x38,0x44,0x44,0x38,0x44,0x44,0x38}, // (22.11) 8
  {0x00,0x38,0x44,0x44,0x3c,0x04,0x44,0x38}, // (22.11) 9
  {0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00}, // (22.11) 10, BLACK
  {0x18,0x3c,0x7e,0xff,0x18,0x18,0x18,0x18}, // (22.11) 11, ARROW OUT, from Z1 to Z2, Z1 means Zone1, Z2 means Zone2
  {0x18,0x18,0x18,0x18,0xff,0x7e,0x3c,0x18}, // (22.11) 12, ARROW IN,  from Z2 to Z1
};
uint8_t JBG_alertCountU8 = 0; // (22.09) alertBeep
//***********************************************************************************************************                  

//***********************************************************************************************************                  
//* (22.11) calling: jb_ledWriteU16_decimalPoint(3478, 1) // (22.11) show '34.78', decimal point location at location 1 of 4 LEDs (0..3)
void jb_ledWriteU16_decimalPoint(uint16_t jb_valueU16In, uint8_t jb_ledIndex_mergePointInU8)
{
  uint8_t  jb_buf[JB_NUMBER_OF_LEDS_4 + 1] = {0}; // + 1 for NULL
  uint16_t jb_valueU16In_tmp = 0;
  uint8_t jb_mergedDecimalPointU8 = 0; // (22.11)  decimal point
  static uint8_t JBL_chU8 = 0; // (22.11) 

  //* extract last 4 digits ONLY into jb_buf[0..3]
  //* for example: input value 3478 => processing => jb_buf[0..3] = {3, 4, 7, 8} 
  jb_valueU16In_tmp = jb_valueU16In % 10000; // show last 4 digits only
  for(int i = 0; i < JB_NUMBER_OF_LEDS_4; i++){ // 0..3
     jb_buf[(JB_NUMBER_OF_LEDS_4 - 1) - i] = (uint8_t)(jb_valueU16In_tmp % 10);  // ALERT: jb_buf[3..0] filled in this order 
     jb_valueU16In_tmp = (uint16_t)(jb_valueU16In_tmp / 10);
  } 
  //* show jb_buf[0..3] on four LEDs
  jb_showAllLeds(MAX7219_SHUTDOWN_REGISTER, MAX7219_OFF_0x00);
  // (22.11) show 4 LEDs
  for(int jb_ledIndex = 0; jb_ledIndex < JB_NUMBER_OF_LEDS_4; jb_ledIndex++){ 
    for (int jb_columnIndex = 0; jb_columnIndex < JB_TABLE_WIDTH_8; jb_columnIndex++){ 
      //***************************************************************************************
      //* merged decimalPoint '.' on specified LED location jb_ledIndex_mergePointInU8
      //***************************************************************************************
      if( (jb_ledIndex == jb_ledIndex_mergePointInU8) && (jb_columnIndex == 7) ){ // (22.11) (22.05) added decimal point
        jb_mergedDecimalPointU8 = 0x01; // (22.11) 0x01 means    decimal point merged  
      }else{
        jb_mergedDecimalPointU8 = 0x00; // (22.11) 0x00 means NO decimal point merged 
      }
      //***********************************
      //**************************************
      //* merged fixed ':' on LED location 1
      //**************************************
      if( (jb_ledIndex == 1) && ((jb_columnIndex == 3) || (jb_columnIndex == 5))  ){ // (22.11) merger ':' on LED Location 1 and COLUME 2 4      
        JBL_chU8 = JB_LED_TABLE_8x8[jb_buf[jb_ledIndex]][jb_columnIndex] | 0x01;
      }else{
        JBL_chU8 = JB_LED_TABLE_8x8[jb_buf[jb_ledIndex]][jb_columnIndex] | jb_mergedDecimalPointU8;        
      }
      jb_showOneLed_8x8(jb_ledIndex, MAX7219_COLUMN_REGISTER(jb_columnIndex), JBL_chU8);
    }
  }
  jb_showAllLeds(MAX7219_SHUTDOWN_REGISTER, MAX7219_ON_0x01);
}
//***********************************************************************************************************                  

//***********************************************************************************************************                  
void jb_ledInit()
{
  for (int i = 0; i < JB_TABLE_WIDTH_8; i++){
    jb_showAllLeds(MAX7219_COLUMN_REGISTER(i), B00000000);
  }
}
//***********************************************************************************************************                  

//***********************************************************************************************************                  
void jb_max7219Init()
{
  // (22.11)  set off
  jb_showAllLeds(MAX7219_DISPLAYTEST_REGISTER, MAX7219_OFF_0x00);
  // (22.11)  set medium intensity
  jb_showAllLeds(MAX7219_INTENSITY_REGISTER, 0x01);
  // (22.11)  set off
  jb_showAllLeds(MAX7219_SHUTDOWN_REGISTER, MAX7219_OFF_0x00);
  // (22.11)  set 8 digits
  jb_showAllLeds(MAX7219_SCANLIMIT_REGISTER, 7);
  // (22.11)  set no decode mode
  jb_showAllLeds(MAX7219_DECODE_REGISTER, B00000000);
  // (22.11)  clear LEDs
  jb_ledInit();
}
//***********************************************************************************************************                  

//***********************************************************************************************************                  
//* show jb_valueU8In value to one LED 8x8 matrix based on MAX7219 driver
void jb_showOneLed_8x8(int jb_indexI16In, uint8_t jb_addressU8In, uint8_t jb_valueU8In)
{
  if ( (jb_indexI16In >= 0) && (jb_indexI16In < JB_NUMBER_OF_LEDS_4) ){ // (22.11) jb_indexI16In must within 0..3
    digitalWrite(JB_DATA_LATCH_PIN_6, LOW);
    delayMicroseconds(100); // (22.11) added little dealy here
    for (int i = JB_NUMBER_OF_LEDS_4 - 1; i >= 0; i--){ // (22.11) 3..0
      if (i == jb_indexI16In){
        shiftOut(JB_DATA_PIN_7, JB_CLOCK_PIN_5, MSBFIRST, jb_addressU8In); 
      }else{
        shiftOut(JB_DATA_PIN_7, JB_CLOCK_PIN_5, MSBFIRST, MAX7219_NOOP_REGITER);
      }     
      shiftOut(JB_DATA_PIN_7, JB_CLOCK_PIN_5, MSBFIRST, jb_valueU8In);
    }  
    delayMicroseconds(100); // (22.11) added little dealy here
    digitalWrite(JB_DATA_LATCH_PIN_6, HIGH);
  }
}
//***********************************************************************************************************                  
 
//***********************************************************************************************************                  
//* show all four LEDs
void jb_showAllLeds(uint8_t jb_addressU8In, uint8_t jb_valueU8In)
{
  digitalWrite(JB_DATA_LATCH_PIN_6, LOW);
  for (int i = 0; i < JB_NUMBER_OF_LEDS_4; i++){
    shiftOut(JB_DATA_PIN_7, JB_CLOCK_PIN_5, MSBFIRST, jb_addressU8In);
    shiftOut(JB_DATA_PIN_7, JB_CLOCK_PIN_5, MSBFIRST, jb_valueU8In);
  } 
  digitalWrite(JB_DATA_LATCH_PIN_6, HIGH);
}
//***********************************************************************************************************                  

//***********************************************************************************************************   
//* KEY DATA PROTOCOL               
//***********************************************************************************************************   
//* (22.11) PROTOCOL: H F D P C T
//* --------------------------------------------------------------------------------
//* Item    Abbre   Name      Location                  Length  Type        Description
//* ---------------------------------------------------------------------------------------------------------
//* 0       H       Header    0                         1       U8          Header('(')
//* 1       F       Frame     1 2 3 4                   4       U32         Frame Number
//* 2       D       Decision  5 6 7 8                   4       U8x4        Decison on Zone1, 2, 3 and 4
//* 3       S       State     9 10                      2       U8x2        Two Independent PATH States
//* 4       C       Counter   11 12 13 14 15 16 17 18   8       U16x4       Four Direction Counter on Two Paths
//* 5       T       Tail      19                        1       U8          Tail (')')
//***********************************************************************************************************                  
void jb_stateMachine(void)
{
  //* define stateName
  #define JB_IDLE_STATE       0
  #define JB_START_STATE      1
  #define JB_HEADER_STATE     2
  static int JBL_state = JB_IDLE_STATE; 
  //* define working buffer
  #define JB_LEN_20 20
  static char JBL_buf[JB_LEN_20 + 1] = {0}; // (22.11) +1 for NULL 
  static uint32_t JBL_bufIndex = 0L;
  static uint8_t JBL_ch = 0;
  #define JB_BLE_HEADER       '('
  #define JB_BLE_TAIL         ')'
  //* compute transit counter between defined Zones
  static uint32_t JBL_FrameNumU32 = 0L;
  static uint32_t JBL_FrameNumU32_old = 999L;
  static uint16_t JBL_C12U16 = 0;
  static uint16_t JBL_C21U16 = 0;
  static uint16_t JBL_targetZoneStateU16 = 0;
  static uint16_t JBL_targetZoneStateU16_tmp = 0; // (22.08) 
  static uint16_t JBL_targetZoneStateU16_old = 1000; // (22.11) for display stable, set default 1000 (set unReachable)
  static uint16_t JBL_showMergedValueU16 = 0; // (22.11)  for 4 LEDs  
  //* mapped JBL_targetZoneStateU16 to LED location, here 5 means outof LED location(DoNothing, not affect on LED display)
  //* location := f(zoneState); [5 2 3 0 1] := f([0 1 2 3 4]) 
  static uint16_t JBL_ledLocation_zoneState_buf[5] = {5, 2, 3, 0, 1}; // (22.08) JBL_targetZoneStateU16 is associated with LED location   
  static int JBL_tinyState = 0;
  static int JBL_iU32 = 0;

  //*************************************************************************************************************************
  switch(JBL_state){
    case JB_IDLE_STATE: 
      JBL_state = JB_HEADER_STATE;
      Serial.print("\n\nJB> REPORT: Two Directions Counter on Path01 (Zone1 and Zone2)\n");
      Serial1.flush(); // (22.11) ignore previous logged data
      jb_ledWriteU16_decimalPoint(0000, 5); // (22.11) init and show 0000, 5 means NO DECIMAL POINT be shown
      break;

   case JB_START_STATE:
    if(Serial1.available()){
      JBL_ch = Serial1.read();
      if(JBL_ch == JB_BLE_HEADER){
        digitalWrite(13, HIGH); // (22.11) on {HEADER} RED LED ON
        JBL_state = JB_HEADER_STATE;
        memset(JBL_buf, 0x00, JB_LEN_20); // (22.11) init JBL_buf[]
        JBL_buf[0] = JB_BLE_HEADER;
        JBL_bufIndex = 1;
        break;             
      }
    }
    break;
    
   case JB_HEADER_STATE:
    if(Serial1.available()){
      JBL_ch = Serial1.read();
      if( (JBL_ch == JB_BLE_TAIL) && (JBL_bufIndex == (JB_LEN_20 - 1)) ){
        JBL_buf[JB_LEN_20 - 1] = JB_BLE_TAIL;
        //********************************************
        //* Extract Counter1(C12) and Counter2(C21)
        //* C12 := count value from Zone1 to Zone2
        //* C21 := count value from Zone2 to Zone1
        //********************************************
        memcpy((char *)(&JBL_FrameNumU32), JBL_buf + 1, 4); 
        memcpy((char *)(&JBL_C12U16), JBL_buf + 11, 2); 
        memcpy((char *)(&JBL_C21U16), JBL_buf + 13, 2); 
        memcpy((char *)(&JBL_targetZoneStateU16), JBL_buf + 9, 2);  // (22.11) (22.03) read state
        //*****************************************
        //* (22.11) for display blinkingLess, on {stateChanged} report JBL_showMergedValueU16 on 4 LEDs 
        if(JBL_targetZoneStateU16 != JBL_targetZoneStateU16_old){
          JBL_targetZoneStateU16_old = JBL_targetZoneStateU16; // (22.11)  update
          //* merged JBL_C12U16 and JBL_C21U16 into one LINE which show at the same time
          JBL_showMergedValueU16 = (uint16_t) ( (JBL_C12U16 % 100) * 100 + (JBL_C21U16 % 100) ); 
          //* show decimalPoint by mapped the LED location from JBL_targetZoneStateU16, location := f(JBL_targetZoneStateU16)
          jb_ledWriteU16_decimalPoint(JBL_showMergedValueU16, JBL_ledLocation_zoneState_buf[JBL_targetZoneStateU16]); // (22.11)  always show point at number 1 LED, (0..3)
        }
        JBL_state = JB_START_STATE;
        memset(JBL_buf, 0x00, JB_LEN_20);         
        digitalWrite(13, LOW); // (22.11)  on {TAIL} RED LED OFF
        break;             
      }else{
        JBL_buf[JBL_bufIndex] = JBL_ch;
        JBL_bufIndex++;
        if(JBL_bufIndex >= 20){
          JBL_state = JB_START_STATE;
          memset(JBL_buf, 0x00, JB_LEN_20);
          JBL_bufIndex = 0;          
        }
      }
    }
    break;
  }
  //*************************************************************************************************************************
  
  //****************************
  //* Report Section
  //****************************
  //* on {frameChanged} show results
  if(JBL_FrameNumU32 != JBL_FrameNumU32_old){
    JBL_FrameNumU32_old = JBL_FrameNumU32;  
    //*****************************************
    //* (22.11)  ALERT: for FOUR LEDs display at the same LINE, merged JBL_C12U16 and JBL_C21U16 
    JBL_showMergedValueU16 = (uint16_t) ( (JBL_C12U16 % 100) * 100 + (JBL_C21U16 % 100) ); 
    //* show on CONSOLE for verifying results   
    Serial.print("JB> (Frame, State, C12, C21, Mergerd) := (");
    Serial.print(JBL_FrameNumU32); 
    Serial.print(", ");
    Serial.print(JBL_targetZoneStateU16);  // 0 1 2 3 4
    Serial.print(", ");
    Serial.print(JBL_C12U16); 
    Serial.print(", ");
    Serial.print(JBL_C21U16); 
    Serial.print(", ");
    Serial.print(JBL_showMergedValueU16);
    Serial.print(", tiny= ");
    Serial.print(JBL_tinyState);
    Serial.print(", iU32= ");
    Serial.print(JBL_iU32);           
    Serial.print(")\n");
    
    #if(1)
    //**********************************************************************************
    //* BEEP Section
    //* Topic: if Counter from Zone1 to Zone2 for every 10 times then alert BEEP  
    //* BNF  : on {JBL_C21U16 % 10 == 0} BEEP for 10 second
    //********************************************************************************** 
    //* tinyStateMachine for alertBeep 
    #define JB_C21_TIMES_10 10
    switch(JBL_tinyState){
      case 0: 
        if(JBL_C21U16 != 0 && JBL_C21U16 % JB_C21_TIMES_10 == 0){
          JBL_iU32 = 0;
          JBL_tinyState = 1;
        }
        break;
  
      case 1: 
        digitalWrite(11, LOW); // beep on 100 ms here
        JBL_tinyState = 2;
        break;
        
      case 2: 
        digitalWrite(11, HIGH); // beep off 100 ms
        if(JBL_iU32++ < 50){ // 0..49 means beep time := 10 sec := 50 * (100 + 100)
          JBL_tinyState = 1;
        }else{
          JBL_tinyState = 3;          
          JBL_iU32 = 0;
        }
        break;
  
      case 3: 
        if(JBL_C21U16 % JB_C21_TIMES_10 != 0){
          JBL_tinyState = 0;
        }
        break;
    }
    #endif
  }  
}
//***********************************************************************************************************   

//***********************************************************************************************************   
void setup()  
{
  //* (1) init Serial for CONSOLE
  Serial.begin(115200); // CONSOLE 
  Serial.print(JB_PROJECT_NAME);
  //* (2) init Serial1 for KEY DATA
  Serial1.begin(115200); // (22.11)  for reading KeyData
  //* (3) init hardware pins for driving MAX2719
  pinMode(JB_CLOCK_PIN_5, OUTPUT);
  pinMode(JB_DATA_LATCH_PIN_6, OUTPUT);    
  pinMode(JB_DATA_PIN_7, OUTPUT);
  //* (4) init MAX2719
  jb_max7219Init();
  //* (5) show version "22.11"
  jb_ledWriteU16_decimalPoint(JB_2211, 1); // 1 means show merged DECIMAL POINT on LED number 1 (LEDs 0..3)
  //* (6) init hardware pins (10:+, 11:out, 12:-), on {powerOn} BEEP 1 sec
  pinMode(10, OUTPUT);
  pinMode(11, OUTPUT);    
  pinMode(12, OUTPUT);
  digitalWrite(10, HIGH); // VCCLike
  digitalWrite(11, LOW);  // signalLike, lowActive
  digitalWrite(12, LOW);  // GNDLike
  delay(1000);
  digitalWrite(11, HIGH);  // signalLike, lowActive  
  delay(2000);  
}
//***********************************************************************************************************                  

//***********************************************************************************************************                  
void loop()
{
  jb_stateMachine();
}
//***********************************************************************************************************                  
 
