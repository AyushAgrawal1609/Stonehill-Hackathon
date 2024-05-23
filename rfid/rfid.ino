//Libraries
#include <SPI.h>//https://www.arduino.cc/en/reference/SPI
#include <MFRC522.h>//https://github.com/miguelbalboa/rfid
#include <WiFi.h>
#include <HTTPClient.h>

const char* ssid = "Redmi 9i";
const char* password = "060d13279482";
const char* serverName = "http://192.168.43.117:3000/newid/";
//Constants
#define SS_PIN 5
#define RST_PIN 0
//Parameters
const int ipaddress[4] = {103, 97, 67, 25};

int t = 0;
//Variables
byte nuidPICC[4] = {0, 0, 0, 0};
MFRC522::MIFARE_Key key;
MFRC522 rfid = MFRC522(SS_PIN, RST_PIN);
void setup() {
 	//Init Serial USB
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

 	Serial.println(F("Initialize System"));
 	//init rfid D8,D5,D6,D7
 	SPI.begin();
 	rfid.PCD_Init();
 	Serial.print(F("Reader :"));
 	rfid.PCD_DumpVersionToSerial();
}


void httpPOSTRequest(String serverName, String httpRequestData) {
  Serial.println("Hello");
  WiFiClient client;
  HTTPClient http;
  http.begin(client, serverName);
  http.addHeader("Content-Type", "application/x-www-form-urlencoded");
  int httpResponseCode = http.POST(httpRequestData);
  http.end();
}

void loop() {
 	readRFID();
}
void readRFID(void ) { /* function readRFID */
 	////Read RFID card
 	for (byte i = 0; i < 6; i++) {
 			key.keyByte[i] = 0xFF;
 	}
 	// Look for new 1 cards
 	if ( ! rfid.PICC_IsNewCardPresent())
 			return;
 	// Verify if the NUID has been readed
 	if ( 	!rfid.PICC_ReadCardSerial())
 			return;
 	// Store NUID into nuidPICC array
 	for (byte i = 0; i < 4; i++) {
 			nuidPICC[i] = rfid.uid.uidByte[i];
 	}
 	Serial.print(F("RFID In dec: "));
 	printDec(rfid.uid.uidByte, rfid.uid.size);
 	Serial.println();
 	// Halt PICC
 	rfid.PICC_HaltA();
 	// Stop encryption on PCD
 	rfid.PCD_StopCrypto1();
}
/**
 		Helper routine to dump a byte array as hex values to Serial.
*/
void printHex(byte *buffer, byte bufferSize) {
 	for (byte i = 0; i < bufferSize; i++) {
 			Serial.print(buffer[i] < 0x10 ? " 0" : " ");
 			Serial.print(buffer[i], HEX);
 	}
}
/**
 		Helper routine to dump a byte array as dec values to Serial.
*/
void printDec(byte *buffer, byte bufferSize) {
  t = 0;
 	for (byte i = 0; i < bufferSize; i++) {
      t+= buffer[i];
 			Serial.print(buffer[i] < 0x10 ? " 0" : " ");
 			Serial.print(buffer[i], DEC);
 	}
   Serial.println(WiFi.status());
  if (WiFi.status() == WL_CONNECTED) {
        String sname = serverName;
        sname += t;
        Serial.print(sname);
        httpPOSTRequest(sname,"");
    } else {
      Serial.println("WiFi Disconnected");
    }
   Serial.print(t);
}