/*
>> Pulse Sensor Amped 1.4 <<
This code is for Pulse Sensor Amped by Joel Murphy and Yury Gitman
	www.pulsesensor.com
	>>> Pulse Sensor purple wire goes to Analog Pin A2 (see PulseSensor_Spark.h for details) <<<

Pulse Sensor sample aquisition and processing happens in the background via a hardware Timer interrupt at 2mS sample rate.
On the Core, PWM on selectable pins A0 and A1 will not work when using this code, because the first allocated timer is TIMR2!
On the Photon, TIMR3 is allocated and has no affect on the A2 pin.

The following variables are automatically updated:
Signal :    int that holds the analog signal data straight from the sensor. updated every 2mS.
IBI  :      int that holds the time interval between beats. 2mS resolution.
BPM  :      int that holds the heart rate value, derived every beat, from averaging previous 10 IBI values.
QS  :       boolean that is made true whenever Pulse is found and BPM is updated. User must reset.
Pulse :     boolean that is true when a heartbeat is sensed then false in time with pin13 LED going out.

This code is designed with output serial data to Processing sketch "PulseSensorAmped_Processing-xx"
The Processing sketch is a simple data visualizer.
All the work to find the heartbeat and determine the heartrate happens in the code below.
Pin D7 LED (onboard LED) will blink with heartbeat.
If you want to use pin D7 for something else, specifiy different pin in PulseSensor_Spark.h
It will also fade an LED on pin fadePin with every beat. Put an LED and series resistor from fadePin to GND.
Check here for detailed code walkthrough:
http://pulsesensor.myshopify.com/pages/pulse-sensor-amped-arduino-v1dot1

Code Version 1.2 by Joel Murphy & Yury Gitman  Spring 2013
This update fixes the firstBeat and secondBeat flag usage so that realistic BPM is reported.

>>> Adapted for Spark Core by Paul Kourany, May 2014 <<<
>>> Updated for Particle Core and Photon by Paul Kourany, Sept 2015 <<<

*/

#include "SparkIntervalTimer.h"
#include <math.h>

void interruptSetup(void);
void serialOutput();
void serialOutputWhenBeatHappens();
void sendDataToSerial(char symbol, int data );
void ledFadeToBeat();
void arduinoSerialMonitorVisual(char symbol, int data );

extern int pulsePin;
extern int blinkPin;
extern volatile int BPM;;
extern volatile int Signal;;
extern volatile int IBI;
extern volatile boolean Pulse;
extern volatile boolean QS;

// Regards Serial OutPut  -- Set This Up to your needs
static boolean serialVisual = false;   // Set to 'false' by Default.  Re-set to 'true' to see Arduino Serial Monitor ASCII Visual Pulse


extern int fadePin;

//Server configuration setup
TCPServer server = TCPServer(23);
TCPClient client;
char inData[128];
char inChar;
char outData[128];
byte i= 0;

//Function that sends commands to clients
void out(const char *s) {
  server.write( (const uint8_t*)s, strlen(s) );
}

//Vib Function Fade Params
double x = 0.00;
double fadeRate = .05;


void setup(){
	//Start server
  server.begin();										// start listening for clients
  Serial.begin(115200);								// Make sure your Serial Terminal app is closed before powering your device
  while(!Serial.available()) Particle.process();  // Now open your Serial Terminal, and hit any key to continue!
  Serial.println(WiFi.localIP());
  Serial.println(WiFi.subnetMask());
  Serial.println(WiFi.gatewayIP());
  Serial.println(WiFi.SSID());

	//Pin Seteup
	pinMode(blinkPin,OUTPUT);         // pin that will blink to your heartbeat!
	pinMode(fadePin,OUTPUT);          // pin that will fade to your heartbeat!
	interruptSetup();                 // sets up to read Pulse Sensor signal every 2mS
}

void loop(){
	serialOutput();
	//Serial.print("Signal:");
	//Serial.println(Signal);
	if (QS == true){     //  A Heartbeat Was Found
		// BPM and IBI have been Determined
		// Quantified Self "QS" true when arduino finds a heartbeat
    x=0;                              //Reset the heart beat counter
		Particle.publish("heartpulseYES","yes");
		digitalWrite(blinkPin,HIGH);     // Blink LED, we got a beat.
		serialOutputWhenBeatHappens();   // A Beat Happened, Output that to serial.
		QS = false;                      // reset the Quantified Self flag for next time
	}
	else {
		digitalWrite(blinkPin,LOW);            // There is not beat, turn off pin 13 LED
		//heartbeat = 0;
		//Particle.publish("heartpulseYES","no");
	}
	ledFadeToBeat();                      // Makes the LED Fade Effect Happen

	if(client.connected()){ 					//If a client (audience) is connected to sever (dancer)
		//Code to Write to clinets
		if (QS == true){
		  //sprintf(outData,"%c","buzz");
			//out(outData);							//out function writes to cliets
      server.write("beat");
      server.write("\n");
      client.flush();								  //flush the remaining bytes that werent read (the carriage return)
		}
	}
	else {
		client=server.available();		//if no clients are connected, then search for more connections
	}
  //delay(1000);                             //  take a break
}


void serialOutput(){   // Decide How To Output Serial.
	if (serialVisual == true){
		arduinoSerialMonitorVisual('-', Signal);   // goes to function that makes Serial Monitor Visualizer
	} else{
		sendDataToSerial('S', Signal);     // goes to sendDataToSerial function
	}
}

//  Decides How To OutPut BPM and IBI Data
void serialOutputWhenBeatHappens(){
	if (serialVisual == true){            //  Code to Make the Serial Monitor Visualizer Work
		Serial.print("*** Heart-Beat Happened *** ");  //ASCII Art Madness
		Serial.print("BPM: ");
		Serial.print(BPM);
		Serial.println("  ");
	} else{
		sendDataToSerial('B',BPM);   // send heart rate with a 'B' prefix
		sendDataToSerial('Q',IBI);   // send time between beats with a 'Q' prefix
	}
}

//  Sends Data to Pulse Sensor Processing App, Native Mac App, or Third-party Serial Readers.
void sendDataToSerial(char symbol, int data ){
	Serial.print(symbol);
  Serial.print(":");
	Serial.println(data);
}

//Maps the analog vib values based on cosine curve
void ledFadeToBeat(){
	double y=cos(x)*255;
  Serial.println(x);
  int z = (int) y;
  analogWrite(fadePin,z);
  if (x > (1.57)) {
    z=0;
    x=1.57;
  }
  else {
    x=x+fadeRate;
  }
  Serial.println(z);
  delay(20);
}

//  Code to Make the Serial Monitor Visualizer Work
void arduinoSerialMonitorVisual(char symbol, int data ){
	const int sensorMin = 0;      // sensor minimum, discovered through experiment
	const int sensorMax = 1024;    // sensor maximum, discovered through experiment

	int sensorReading = data;
	// map the sensor range to a range of 12 options:
	int range = map(sensorReading, sensorMin, sensorMax, 0, 11);

	// do something different depending on the
	// range value:
	switch (range) {
	case 0:
		Serial.println("");     /////ASCII Art Madness
		break;
	case 1:
		Serial.println("---");
		break;
	case 2:
		Serial.println("------");
		break;
	case 3:
		Serial.println("---------");
		break;
	case 4:
		Serial.println("------------");
		break;
	case 5:
		Serial.println("--------------|-");
		break;
	case 6:
		Serial.println("--------------|---");
		break;
	case 7:
		Serial.println("--------------|-------");
		break;
	case 8:
		Serial.println("--------------|----------");
		break;
	case 9:
		Serial.println("--------------|----------------");
		break;
	case 10:
		Serial.println("--------------|-------------------");
		break;
	case 11:
		Serial.println("--------------|-----------------------");
		break;

	}
}
