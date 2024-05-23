#include <WiFi.h>
#include <HTTPClient.h>
long duration;
long distance;
const char* ssid = "Redmi 9i";
const char* password = "060d13279482";
const char* serverName = "http://192.168.43.117:3000/output/sensor";
long lastTime;

void setup() {  
  Serial.begin(115200);
  WiFi.begin(ssid, password);
  Serial.println("Connecting");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.print("Connected to WiFi network with IP Address: ");
  Serial.println(WiFi.localIP());

  // put your setup code here, to run once:
  pinMode(33,OUTPUT);
  pinMode(17,OUTPUT);
  pinMode(25,OUTPUT);
  pinMode(27,OUTPUT);
  pinMode(32,INPUT);
}

void httpPOSTRequest(const char* serverName, String httpRequestData) {
  WiFiClient client;
  HTTPClient http;
  http.begin(client, serverName);
  http.addHeader("Content-Type", "application/x-www-form-urlencoded");
  int httpResponseCode = http.POST(httpRequestData);
  http.end();
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
    if(distance<40){
      digitalWrite(25, HIGH);
    }else{
      digitalWrite(25, LOW);
    }
    if(distance<20){
      digitalWrite(27, HIGH);
    }else{
      digitalWrite(27, LOW);
    }
    if(distance<15){
      digitalWrite(17, HIGH);
    }else{
      digitalWrite(17, LOW);
    }
    if(millis()-lastTime>2000){
          String w = "distance=";
          w+= distance;
          if (WiFi.status() == WL_CONNECTED) {
            httpPOSTRequest(serverName, w);

    } else {
      Serial.println("WiFi Disconnected");
    }

    }
}
