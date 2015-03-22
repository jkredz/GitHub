//Maxim Integrated Max4618 Multiplexer

int B = 0;      
int A = 0;  // the two digital pins for the bits     

String data;
String data1;

 
/* Truth Table      
 B A On Switches
 0 0 X0,Y0 (Left x-accel , Right x-accel)
 0 1 X1,Y1 (Left y-accel , Right y-accel)
 1 0 X2,Y2 (Left z-accel , Right z-accel)
 1 1 X3,Y3 (NOT USED)
 
 
 */
int  bin [] = {00, 01, 10};//list of binary values
 
void setup(){
 
  //Pin output
  pinMode(10, OUTPUT);    // B
  pinMode(11, OUTPUT);    // A
  
  //Acc Sensor Input Setup
  pinMode(0, OUTPUT); //Leg Left input
  pinMode(1, OUTPUT); //Leg Right input
  pinMode(2, OUTPUT); //Ankle Left input
  pinMode(3, OUTPUT); //Ankle Right input
  pinMode(5, OUTPUT); //Thigh Left input
  pinMode(6, OUTPUT); //Thigh Right input
  
  Serial.begin(9600); // fire up the serial
  Serial.println("Left Leg X, Right Leg X, Left Ankle X, Right Ankle X, Left Thigh X, Right Thigh X; Left Leg Y, Right Leg Y, Left Ankle Y, Right Ankle Y, Left Thigh Y, Right Thigh Y; Left Leg Z, Right Leg Z, Left Ankle Z, Right Ankle Z, Left Thigh Z, Right Thigh Z");  
  
}
 
  
void loop () {
 for (int count=0; count < 3; count++) { //loop through each channel, checking for a signal
    
   int row = bin[count]; //channel 5 = 5th element in the bin list -> 101 etc. 
    
   B = bitRead(row,1); //bitRead() -> parameter 1 = binary sequence, parameter 2 = which bit to read, starting from the right most bit
   A = bitRead(row,0); //channel 7 = 111, 1 = 2nd bit 
   
 
   digitalWrite(10, B); // send the bits to the digital pins 
   digitalWrite(11, A);
   
       
   Serial.print(count);
   Serial.print(" ==== ");
   
   int x[6];
   
   for (int sensor=0; sensor < 6; sensor++){ //loop through reading each accelerometer sensor data
     analogWrite(sensor, 255);
     delay(1000);
     //data=String(analogRead(sensor));
     data1 += data + " , ";
   }
  
  data1= data1 + "; ";
 }
 Serial.println(data1);
 data1="";  
 delay (1000); // time to read the values
}
 
 
