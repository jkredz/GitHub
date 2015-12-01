// This #include statement was automatically added by the Particle IDE.
#include "Thermistor.h"
int sendMessage(String command);

//jst thermistor
float c1=.001468, c2=.0002383 , c3=.0000001007;
//float c1=.0008236945712, c2=.0002632511198 , c3=.0000001349588752;  //Steinhart Coefficient for 103JT-025
String tempFval;
int boardLed = D7;
int thermPin = A0;
int thermRes = 9750;
int analogvalue;
Thermistor Thermistor(thermPin, thermRes);

// Exposed variables
double tempF = 0.0;
int lol = 10000;

void setup() {
  Serial.begin(9600);
  Particle.variable("analogvalue", analogvalue);
  Particle.variable("tempF",tempF);
  Particle.variable("lol",lol);

  //Particle.function("sendMessage", sendMessage);
  Thermistor.begin();
}

void loop() {
  tempF = Thermistor.getTempF(true);
  Serial.println(tempF);
  if (tempF > 78){
      tempFval=String(tempF);
      Particle.publish("libratojc_test",tempFval);
      digitalWrite(boardLed,HIGH);
      delay(500);
      digitalWrite(boardLed,LOW);
      Serial.println("data sent");
  }

  delay(5000);
}

/*
int sendMessage(String command)
{
    Spark.publish("twilio", "Hi", 60, PRIVATE);
}
*/
void serialEvent()
{
    char c = Serial.read();
    Serial.println(c);
}
