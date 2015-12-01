/*
###################################################################
This code is the audience_spark controller that receives commands and
-gets posts from the cloud
-vibrates based on received heart rate values

Commands
-HRR_STATE turn on Audience Spark's  HR Subscriber
###################################################################
*/

boolean HRRSTATE;
int faderate;

void setup() {
  Serial.begin(9600);
  Particle.function("HRR_STATE", HRR_STATE);
  pinMode(D0,OUTPUT);
  pinMode(D7,OUTPUT);
  Particle.variable("heartbeat", INT);   //Look at the variable heartbeat to see if it exists
}

void loop() {
  if (HRRSTATE==true){
    Serial.println("HRR is turned on");
    if (heartbeat == 1){
      fadeRate=255;                      //if a beat is registered (heartbeat=1) then LED pin analog value
    }
  }
  ledFadeToBeat();                       // Makes the LED Fade Effect Happen
  delay(20);                             //  take a break
}


//Listens on the cloud for the command to turn on read the Heart Rate Stream
int HRR_STATE(String command) {
    if (command=="on") {
        digitalWrite(D0,HIGH);
        HRRSTATE = true;
        return 1;
    }
    else if (command=="off") {
        digitalWrite(D0,LOW);
        HRRSTATE = false;
        return 0;
    }
    else {
        return -1;
    }
  }

//Function that controls what the LED or Vibration should do based on incoming heart beat
void ledFadeToBeat(){
	fadeRate -= 15;                         //  set LED fade value
	fadeRate = constrain(fadeRate,0,255);   //  keep LED fade value from going into negative numbers!
	analogWrite(fadePin,fadeRate);          //  fade LED
}
