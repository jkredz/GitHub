//0G Bias Test.  Leave the accelerometer on the table.  note, that direction facing down will experience 1G Gravity
//Program calculates the G from analog read values.

const float biasx0 = 1500.0; //measured bias mV of x-accelerometer 0  
const float incx0 = 279.0; //measured mV/G of x-accelerometer 0

const float biasy0 = 1500.0; //measured bias mV of y-accelerometer 0  
const float incy0 = 279.0; //measured mV/G of y-accelerometer 0

const float biasz0 = 1500.0; //measured bias mV of z-accelerometer 0
const float incz0 = 279.0; //measured mV/G of z-accelerometer 0

int xpin = A0;         // x-axis of the accelerometer
int ypin = A1;         // y-axis
int zpin = A2;         // z-axis (only on 3-axis models)

//variables of analog read of accelerometers
int xVal = 0;
int yVal = 0;
int zVal = 0;

//variables of calculated mV of accelerometers
float xV;
float yV;
float zV;


//variables for measured g of accelerometers
float xG;
float yG;
float zG;
String one, two, three, a;
void setup()
{
    pinMode(xpin, INPUT);
    pinMode(ypin, INPUT);
    pinMode(zpin, INPUT);
    a = String();
    Serial.begin(9600);
}

void loop() 
{
  
    
    xVal = analogRead(xpin);
    yVal = analogRead(ypin);
    zVal = analogRead(zpin);
    one = String("Analog Read Values: "); 
    a = one + " " + xVal + " " + yVal + " " + zVal;
    Serial.println(a);
   
   xV=bittomV(xVal); //calculated x accelerometer mV 
   yV=bittomV(yVal);
   zV=bittomV(zVal);
   two = String("Measured mV: ");
   a = two + " " + xV + " " + yV + " " + zV;
   Serial.println(a);
   

 //Calculate g of accelerometers
   xG=(xV-biasx0)/incx0;
   yG=(yV-biasy0)/incy0;
   zG=(zV-biasz0)/incz0;
   three = String("Calculated accelerometer g: ");
   a = three + xG + " " + yG + " " + zG;
   Serial.println(a);
 
 delay(5000);
    
}

float bittomV(int a){
float result;

result=a/1023.00*5.00*1000.00;
return result;
}
