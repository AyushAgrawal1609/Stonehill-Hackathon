long duration;
long distance;
void setup() {
  Serial.begin(115200);
  // put your setup code here, to run once:
  pinMode(33,OUTPUT);
  pinMode(32,INPUT);
}

void loop() {
  // put your main code here, to run repeatedly:
    digitalWrite(33, LOW);
    delayMicroseconds(2);
    digitalWrite(33, HIGH);
    delayMicroseconds(10);
    digitalWrite(33, LOW);
    duration = pulseIn(32, HIGH);
    distance = duration * 3.4 / 200;
    Serial.println(distance);
    
}
