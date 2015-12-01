// -----------------------------------------
// Publish and Subscribe
/* -----------------------------------------

We are going to Spark.publish a public event to the cloud.
That means that everyone can see you event and anyone can subscribe to it.
You and your buddy will both publish an event, and listen for each others events.

------------------------------------------*/

int vib = A0;
int time;


// We start with the setup function.

void setup() {
  Serial.begin(9600);
  pinMode(vib,OUTPUT); // Our vib pin is output
  // Here we are going to subscribe to your buddy's event using Spark.subscribe
  Spark.subscribe("librato_A0", myHandler);
  // Subscribe will listen for the event buddy_unique_event_name and, when it finds it, will run the function myHandler()
  // myHandler() is declared later in this app.
}


void loop() {
}


// Now for the myHandler function, which is called when the cloud tells us that our buddy's event is published.
void myHandler(const char *event, const char *data)
{
  Serial.print("data: ");
  Serial.println(data);
  float data_received = atof(data);
  Serial.print("data_received: ");
  Serial.println(data_received);
  if (data_received > 80) {
    //Serial.println(data_received);
    time = map(data_received, 80, 90, 500, 2000);
    analogWrite(vib,255);
	  delay(time);
  }
}
