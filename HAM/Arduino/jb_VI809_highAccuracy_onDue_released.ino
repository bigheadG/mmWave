//****************************************************************************************************************
//* jb_VI809_highAccuracy_onDue_released.ino 
//* Prerequisite: (1) Software: Arduino IDE V1.8.10 (or later version)
//*               (2) Hardware: Arduino DUE board
//*                             Install Library of "FastLED V3.3.2"
//*                             LED strip of WS2812B (with power supply 5 volts INDEPENDENT), DATA pin is connected to DUE's pin11
//* Notes:  (1) Calibration: 
//*             you may fine tune as calibration by function of map() regarding on JBG_distanceF32 and JB_1M_PER_NUM_LED_61
//*             you should measure how many LEDs in ONE meter due to different puchased LED STRIP may have different LEDs number  
//*         (2) set maximun distance upto 2660 mm with upper limit here
//*         (3) for watchDog, on {1 sec HangUp} reStart DUE board to avoid HANG UP in case
//* Refer:  (1) for fastLedLib library, https://github.com/FastLED/FastLED
//*         (2) for watchDog on DUE only, https://forum.arduino.cc/index.php?topic=506052.0
//*         (3) for UART port, https://blog.startingelectronics.com/how-to-use-arduino-serial-ports/
//* Report: report on console and looks as following,
//*         JB> flow= 154, measured= 397.22 mm, LedLoaction= 24
//****************************************************************************************************************
#define JB_PROJECT_NAME "\n\n\nJB> jb_VI809_highAccuracy_onDue_released.ino 2020.10.16"
//****************************************************************************************************************
//* ALERT: you should measure the value how many LEDs in one meter due to different LED STRIP may be had the different number
#define JB_1M_PER_NUM_LED_61  (61)    // ALERT: should be mapped to (LED_LOCATION / METER) := (61 leds / 1 meter) depends
#define JB_MAX_NUM_LEDS_266   (266)   // max LEDs number in this lab
#define JB_DISTANCE_2_66M     (2.66f) // max range in this lab
#define JB_DISTANCE_1_00M     (1.00f)  
#define JB_KEYDATA_HEADER     ('.') 
#define JB_KEYDATA_TAIL       (':') 
#define JB_DATA_PIN_11        (11)    // connect to WS2812B DIN data input port
#define JB_BAUD_115200        (115200)  // set baud rate as 115200/8/n/1
//****************************************************************************************************************
#include <FastLED.h>
CRGBArray<(JB_MAX_NUM_LEDS_266 + 1)> leds;
//* STATE MACHINE SECTION
#define JB_IDLE_STATE       0
#define JB_START_STATE      1
#define JB_HEADER_STATE     2
#define JB_REPORT_STATE     3
int JBG_state = JB_IDLE_STATE;
#define JB_LEN_20           20
uint32_t JBG_bufIndex = 0;
char JBG_buf[JB_LEN_20] = {0};
float JBG_distanceF32 = 0.0f;
uint32_t JBG_flowU32 = 0L;
uint32_t JBG_ledU32 = 0L;
uint32_t JBG_ledU32Old = 0L;
uint32_t JBG_ledStartU32 = 0L;
uint32_t JBG_ledEndU32 = 0L;
int i = 0;

//************************************************************************************************************
//* W A T C H D O G    S E C T I O N
//************************************************************************************************************
//************************************************************************************************************
#define JBG_SEC_1   (1)
#define WDT_KEY     (0xA5)
void jb_watchDogInitSec(uint8_t jb_secIn)
{
  // Enable watchdog.
  WDT->WDT_MR = WDT_MR_WDD(0xFFF)
                | WDT_MR_WDRPROC
                | WDT_MR_WDRSTEN
                | WDT_MR_WDV(256 * (jb_secIn) ); // Watchdog triggers a reset after N seconds if underflow
                                       // for example: 2 seconds equal 84000000 * 2 = 168000000 clock cycles
}
//************************************************************************************************************

//************************************************************************************************************
void jb_watchDogReStart()
{
  //Restart watchdog
  WDT->WDT_CR = WDT_CR_KEY(WDT_KEY) | WDT_CR_WDRSTT;
}
//************************************************************************************************************

//************************************************************************************************************
//* S T A T E    M A C H I N E    S E C T I O N 
//************************************************************************************************************
//************************************************************************************************************
void jb_stateMachine(void)
{
  static uint8_t JBL_hue;
  static uint8_t JBL_ch = 0;
  
  switch(JBG_state){
    case JB_IDLE_STATE: 
      JBG_state = JB_HEADER_STATE;
      break;

   case JB_START_STATE:
    if(Serial1.available()){
      JBL_ch = Serial1.read();
      if(JBL_ch == JB_KEYDATA_HEADER){ // '.'
        digitalWrite(13, HIGH);
        JBG_state = JB_HEADER_STATE;
        memset(JBG_buf, 0x00, JB_LEN_20); // init JBG_buf[]
        JBG_buf[0] = JB_KEYDATA_HEADER;
        JBG_bufIndex = 1;
        break;             
      }
    }
    break;
    
   case JB_HEADER_STATE:
    if(Serial1.available()){
      JBL_ch = Serial1.read();
      if(JBL_ch == JB_KEYDATA_TAIL && JBG_bufIndex == 19){ // byte 19 means end of KEY data per frame  
        JBG_buf[19] = JB_KEYDATA_TAIL; // ':'
        JBG_state = JB_REPORT_STATE;
        break;             
      }else{
        JBG_buf[JBG_bufIndex] = JBL_ch; // save to buffer
        JBG_bufIndex++;
      }
    }
    break;

    case JB_REPORT_STATE:
      //* report: on {50 ms} show flow, distance and ledLocation
      memcpy((char *)(&JBG_distanceF32), JBG_buf + 8, 4); // convert as distance (unit: m) 
      Serial.print("JB> flow= ");
      Serial.print(JBG_flowU32++); 
      Serial.print(", measured= ");
      Serial.print(JBG_distanceF32 * 1000, 2); // show float value with TWO floating digit (uint: mm)
      Serial.print(" mm");           
      digitalWrite(13, LOW); // blinking LED
      if(JBG_distanceF32 >= JB_DISTANCE_2_66M){
        JBG_distanceF32 = JB_DISTANCE_2_66M; // upper limit
      }
      //****************************************************************************
      JBG_ledU32 = map(JBG_distanceF32 * 1000, 0, JB_DISTANCE_1_00M * 1000, 0, JB_1M_PER_NUM_LED_61 - 1); // mm => ledLocation
      //****************************************************************************      
      Serial.print(", LedLoaction= ");
      Serial.println(JBG_ledU32 + 1); // +1 for count from 1
      //**********************************************************************
      //* ledGapFillingMethod: looks like some LEDs fading and dimming when TARGET is moving
      //* updated led START and END location  
      if(JBG_ledU32 >= JBG_ledU32Old){
         JBG_ledStartU32 = JBG_ledU32Old;
         JBG_ledEndU32 = JBG_ledU32;
      }else{
         JBG_ledStartU32 = JBG_ledU32;
         JBG_ledEndU32 = JBG_ledU32Old;        
      }
      JBG_ledU32Old = JBG_ledU32; 
      //* show on LEDs
      for(int j = 0; j < JBG_ledStartU32; j++) { 
        leds[j] = 0; 
      }  
      for(int j = JBG_ledStartU32; j < JBG_ledEndU32; j++) { 
        leds.fadeToBlackBy(80);
        leds[j] = CHSV(JBL_hue++, 255, 255);
      }  
      leds.fadeToBlackBy(10);
      leds[JBG_ledEndU32] = CHSV(JBL_hue++, 255, 255);
      FastLED.delay(1);
      //**********************************************************************
      JBG_state = JB_START_STATE;
      break;
  }
}
//************************************************************************************************************
 
//************************************************************************************************************
void setup() { 
  //* Define SERIAL ports
  Serial.begin(JB_BAUD_115200);   // for CONSOLE
  Serial.println(JB_PROJECT_NAME);
  Serial1.begin(JB_BAUD_115200);  // for KEY data
  //* Set LED blinking for receiving KeyData 
  pinMode(13, OUTPUT);
  digitalWrite(13, LOW);
  //* Define ledString: WS2812B, connect DUE's pin11 to WS2812B's DIN pin
  FastLED.addLeds<WS2812B, JB_DATA_PIN_11, RGB>(leds, JB_MAX_NUM_LEDS_266); // define MOSI pin at 11
  //* initWatchDog
  jb_watchDogInitSec(JBG_SEC_1);  // set 1 sec
}
//************************************************************************************************************

//************************************************************************************************************
void loop(){ 
  jb_watchDogReStart(); // to avoid CPU HANG up in case
  jb_stateMachine();    // run state machine
}
//************************************************************************************************************
