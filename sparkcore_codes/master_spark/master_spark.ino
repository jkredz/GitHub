/*
###################################################################
This code is the master_spark controller that sends commands to the
-Dancer Spark
-Audience Spark

Commands
-HRR_STATE turn on Audience Spark's  HR Subscriber
-HRP_STATE turn on Dancer Spark's HR Poster
###################################################################
*/

boolean HRRSTATE;
boolean HRPSTATE;

void setup() {
  Serial.begin(9600);
  Particle.function("HRP_STATE", HRP_STATE);
  Particle.function("HRR_STATE", HRR_STATE);
  pinMode(D0,OUTPUT);
  pinMode(D7,OUTPUT);
}

void loop() {
  if (HRRSTATE==true){
    Serial.println("HRR is turned on");
  }
  if (HRPSTATE==true){
    Serial.println("HRP is turned on");
  }
}

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

int HRP_STATE(String command) {
    if (command=="on") {
        digitalWrite(D7,HIGH);
        HRPSTATE=true;
        return 1;
    }
    else if (command=="off") {
        digitalWrite(D7,LOW);
        HRPSTATE=false;
        return 0;
    }
    else {
        return -1;
    }
}
